# -*- coding: utf-8 -*-
# Copyright 2021 Cardiff University
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""HTCondor interface for IGWN Accounting
"""

import datetime
import json
import re
import subprocess
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from pathlib import Path
from shutil import which
from socket import getfqdn

from dateutil import tz

import htcondor

from ..utils import (
    DEFAULT_LOGGER as LOGGER,
    datetime_from_epoch,
)
from . import BatchSystem

try:
    from htcondor import HTCondorException
except ImportError:  # htcondor < 8.9.0
    HTCondorException = RuntimeError

__author__ = "Duncan Macleod <duncan.macleod@ligo.org>"

# date handling
UTC = tz.tzutc()
LOCAL = tz.tzlocal()
NOW = datetime.datetime.utcnow().replace(
    microsecond=0,
    tzinfo=UTC,
)
TODAY = NOW.replace(hour=0, minute=0, second=0)
YESTERDAY = TODAY + datetime.timedelta(days=-1)

# condor history data
IGWN_USER_CLASSAD = "LigoSearchUser"
IGWN_TAG_CLASSAD = "LigoSearchTag"
HISTORY_CLASSADS = [
    IGWN_USER_CLASSAD,
    IGWN_TAG_CLASSAD,
    "AccountingGroup",
    "CompletionDate",
    "CpusProvisioned",
    "CumulativeSuspensionTime",
    "EnteredCurrentStatus",
    "ExitCode",
    "MATCH_GLIDEIN_Site",
    "MaxHosts",
    "Owner",
    "RemoteWallClockTime",
    "RequestCpus",
]
LOCAL_GLIDEIN_SITE_ID = (
    "unknown",
    "undefined",
)

# regex to find history warnings
BAD_HISTORY_REGEX = re.compile(
    r"(\s+)?\*\*\*\s+"
)


# -- condor interactions ----

def get_condor_version(executable=None):
    """Call condor_version and return the output

    Parameters
    ----------
    executable : `str`, optional
        the path to the condor_version executable to call,
        defaults to the first one on the ``PATH``

    Returns
    -------
    text : `str`
        the decoded text from ``condor_version``

    Examples
    --------
    >>> print(get_condor_version())
    $CondorVersion: 8.8.5 Sep 04 2019 BuildID: 480168 PackageID: 8.8.5-1 $
    $CondorPlatform: x86_64_RedHat7 $
    """
    return subprocess.check_output(
        [executable or which("condor_version")],
    ).decode("utf-8").strip()


def get_condor_version_number(executable=None):
    """Call condor_version and return the version number.

    Parameters
    ----------
    executable : `str`, optional
        the path to the condor_version executable to call,
        defaults to the first one on the ``PATH``

    Returns
    -------
    version : `str`
        the version number stripped from the output of ``condor_version``

    See also
    --------
    get_condor_version
        for details of the call to ``condor_version``

    Examples
    --------
    >>> print(get_condor_version_number())
    8.8.5
    """
    try:
        if executable:  # if given, always query from CLI
            raise AttributeError
        return htcondor.__version__
    except AttributeError:
        raw = get_condor_version(executable=executable)
        cvregex = re.compile(r"(\s|\A)(\d+\.\d+\.\d+([a-z0-9]+)?)(\s|\Z)")
        return cvregex.search(raw).group().strip()


def find_schedulers(pool=None):
    """Returns the names of all schedulers known by the condor collector
    """
    coll = htcondor.Collector(pool)
    scheds = [
        schedd["name"] for
        schedd in coll.locateAll(htcondor.DaemonTypes.Schedd)
    ]
    if not scheds:
        raise RuntimeError(
            "condor_status did not return any schedd names",
        )
    return scheds


# -- condor history query -----------------------

def parse_job(job, cluster):
    """Parse the information about a job into what we want

    Returns
    -------
    owner : `str`
        the name of the job owner
    tag : `str`
        the search tag used
    cpu_hours : `float`
        the total cost of this job in CPU hours
    cluster : `str`
        the name of the cluster to use in the accounting

    Notes
    -----
    The ``cpu_hours`` is calculated as

        (RemoteWallclockTime - CumulativeSuspensionTime)
        * MaxHosts
        * RequestCpus
        / hour
    """
    owner = job.get(IGWN_USER_CLASSAD, job.get("Owner", "UNKNOWN"))
    tag = job.get(IGWN_TAG_CLASSAD, job.get("AccountingGroup", "UNDEFINED"))
    # parse job end date
    end = float(job["CompletionDate"]) or float(job["EnteredCurrentStatus"])
    enddate = datetime_from_epoch(end).strftime("%Y-%m-%d")
    # get hosts
    hosts = float(job.get("MaxHosts", 1))
    # get cpus
    try:
        cpus = float(job["CpusProvisioned"])
    except (KeyError, ValueError):
        cpus = float(job.get("RequestCpus", 1))
    # get total job time (seconds)
    runtime = (
        float(job["RemoteWallClockTime"]) -
        float(job["CumulativeSuspensionTime"])
    )
    # if the job didn't get assigned a MATCH_GLIDEIN_Site,
    # then it ran in the local pool
    site = job.get("MATCH_GLIDEIN_Site")
    if site and site.lower() not in LOCAL_GLIDEIN_SITE_ID:
        cluster = "OSG.{}".format(site)

    return owner, tag, hosts * cpus * runtime / 3600., enddate, cluster


def get_history(
        schedname,
        cluster,
        start,
        end,
        classads=HISTORY_CLASSADS,
        constraints=None,
        pool=None,
        file=None,
):
    """Query for all jobs that completed in the given interval

    Parameters
    ----------
    schedname : `str`
        the (host)name of the scheduler to query

    cluster : `str`
        the name of the cluster to use in the accounting

    start : `float`
        the Unix epoch start of the relevant interval

    end : `float`
        the Unix epoch end of the relevant interval

    classads : `list` of `str`
        the list of classads to return for each job

    constraints : `list` of `str`
        extra constraint expressions to be used in this
        query; constraints are added using ``'&&'`` meaning
        jobs must match all constraints

    pool : `str`, optional
        the name of the condor pool to use

    file : `str`, optional
        the path of a specific condor_history file to use

    Returns
    -------
    history : `iterable` of `dict`
        the raw output from :meth:`htcondor.Schedd.history`
    """
    constraints = (
        "JobUniverse != 7",
        "Owner != \"igwn-pilot\"",
        "JobFinishedHookDone >= {}".format(start),
        "JobFinishedHookDone < {}".format(end),
    ) + tuple(constraints or [])
    constraint_expr = " && ".join(constraints)
    args = (schedname, constraint_expr, classads, None, pool)

    # print what's about to happen
    LOGGER.debug("History query parameters:")
    LOGGER.debug("  since: None")
    LOGGER.debug("  constraints:")
    for constraint in sorted(constraints):
        LOGGER.debug("    {!r}".format(constraint))
    LOGGER.debug("  classads:")
    for ad_ in sorted(classads):
        LOGGER.debug("    {!r}".format(ad_))

    # if given a history file, we can only use condor_history
    # on the command line
    if file:
        for job in _get_history_subprocess(*args, file):
            yield parse_job(job, cluster=cluster)
        return

    # otherwise we can try using python first
    try:
        history = _get_history_python(*args)
        for job in history:
            yield parse_job(job, cluster=cluster)
    except HTCondorException as exc:
        LOGGER.warning(
            "history query using python API failed: {}, "
            "retrying using condor_history executable [{}]".format(
                str(exc),
                schedname,
            ),
        )
        for job in _get_history_subprocess(*args):
            yield parse_job(job, cluster=cluster)


def _get_history_python(schedname, constraint, classads, since, pool):
    try:
        schedd_ad = htcondor.Collector(pool).locate(
            htcondor.DaemonTypes.Schedd,
            schedname,
        )
        schedd = htcondor.Schedd(schedd_ad)
    except HTCondorException:
        # raise proper exceptions normally,
        # this just serves to allow us to separate out ValueErrors
        # that are raised by htcondor < 8.9.0, see below
        # NOTE: this except block can be entirely removed if we get
        #       as far as requiring htcondor >= 8.9.0
        raise
    except ValueError as exc:
        # if htcondor < 8.9.0, translate a ValueError into a
        # RuntimeError so that we can separate it from any other
        # ValueErrors we might get from job parsing or similar
        # NOTE: this block can be entirely removed if we get
        #       as far as requiring htcondor >= 8.9.0
        raise HTCondorException(str(exc)) from exc
    LOGGER.debug("Executing python history query")
    return schedd.history(
        constraint,
        projection=classads,
        since=since,
    )


def _get_all_history(schedulers, *args, error=True, **kwargs):
    """Yield all jobs from all schedulers
    """
    for sched in schedulers:
        yield from _handle_history(
            get_history(sched, *args, **kwargs),
            sched,
            error=error,
        )


def _handle_history(iterator, sched, error=True, iterate=True):
    try:
        yield from iterator
    except (RuntimeError, ValueError) as exc:
        exc.args = (str(exc) + " [{}]".format(sched),)
        if error:
            LOGGER.critical(str(exc))
            raise
        LOGGER.warning(str(exc))
    else:
        LOGGER.debug("Data received from {}".format(sched))


# -- 'manual' condor_history query --------------

def _get_history_subprocess(
        schedname,
        constraint,
        classads,
        since,
        pool,
        file=None,
):
    condor_version = get_condor_version_number()
    htcondor_89 = condor_version >= "8.9.0"
    cmd = [
        which("condor_history"),
        "-constraint", constraint,
    ]
    if since:
        cmd.extend(("-since", since))
    if schedname != getfqdn():
        cmd.extend(("-name", schedname))
    if htcondor_89:  # htcondor >=8.9.0
        cmd.extend(["-jsonl", "-af"] + classads)
    else:  # htcondor < 8.9.0
        cmd.extend(_format_condor_history_classads(classads))
    if pool:
        cmd.extend(("-pool", pool))
    if file:
        cmd.extend(("-file", file))
    cmdstr = " ".join(repr(x) if ' ' in x else x
                      for x in cmd)
    LOGGER.debug("Executing condor_history")
    LOGGER.debug("  $ {}".format(cmdstr))
    load_json = json.loads
    for line in subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            check=True,
    ).stdout.splitlines():
        line = line.decode("utf-8")
        try:
            data = load_json(line)
        except json.JSONDecodeError:
            if BAD_HISTORY_REGEX.match(line):
                LOGGER.warning(line.lstrip(r"\t* "))
                continue
            raise
        if not htcondor_89:  # htcondor < 8.9.0
            for key in list(data.keys()):
                if data[key] == "undefined":  # just ignore undefined classads
                    del data[key]
        yield data


def _format_condor_history_classads(classads):
    """Returns a list of `-format <str> <classad>` arguments for condor_history

    Notes
    -----
    This is only required to support htcondor < 8.9.0 and can be removed when
    we can require htcondor >=8.9.0
    """
    args = [
        "-format",
        "{{\"{}\": \"%v\", ".format(classads[0]),
        classads[0],
    ]
    for classad in classads[1:-1]:
        args.extend((
            "-format",
            "\"{}\": \"%v\", ".format(classad),
            classad
        ))
    args.extend((
        "-format",
        "\"{}\": \"%v\"}}\\n".format(classads[-1]),
        classads[-1],
    ))
    return args


# -- wrappers for multi processing --------------

def _get_history_mp(sched, *args, error=True, **kwargs):
    return list(_handle_history(
        get_history(sched, *args, **kwargs),
        sched,
        error=error,
        iterate=False,
    ))


def _get_all_history_mp(
        nproc,
        schedulers,
        cluster,
        start,
        end,
        **kwargs
):
    _get_history = partial(
        _get_history_mp,
        cluster=cluster,
        start=start,
        end=end,
        **kwargs
    )
    with ProcessPoolExecutor(nproc) as pool:
        for result in pool.map(_get_history, schedulers):
            yield from result


# -- interface ----------------------------------

class HTCondor(BatchSystem):
    """`BatchSystem` implementation for HTCondor.
    """
    name = "HTCondor"

    @staticmethod
    def get_jobs(
        start,
        end,
        schedulers=None,
        parallel=1,
        pool=None,
        condor_history_file=None,
        constraints=None,
        error=True,
        cluster=None,
    ):
        """Query the HTCondor history for jobs

        Parameters
        ----------
        start : `float`
            the Unix epoch start of the relevant interval

        end : `float`
            the Unix epoch end of the relevant interval

        schedulers : `list` of `str`, optional
            the list of scheduler hostnames to query, default is
            to query all schedulers in the ``pool``

        pool : `str`, optional
            the name of the HTCondor pool to use, only used to
            query the collector for schedd names

        parallel : `int`, optional
            number of parallel processes to use when querying for
            history from multiple schedds.

        condor_history_file : `str`, optional
            path of HTCondor history file to use when reading history
            information

        constraints : `list` of `str`
            extra constraint expressions to be used in this
            query; constraints are added using ``'&&'`` meaning
            jobs must match all constraints

        error : `bool`, optional
            if `True` raise exceptions as they occur, otherwise
            only emit warnings

        cluster : `str`
            name of cluster to use in formatting job information
        """
        if schedulers is None:
            schedulers = find_schedulers(pool)

        if parallel > 1:
            _getter = partial(_get_all_history_mp, parallel)
        else:
            _getter = _get_all_history

        yield from _getter(
            schedulers,
            cluster,
            start,
            end,
            error=error,
            pool=pool,
            file=condor_history_file,
            constraints=constraints,
        )

    @staticmethod
    def get_system_version():
        if Path("/usr/bin/condor_version").exists():
            return get_condor_version("/usr/bin/condor_version")
        return get_condor_version()

    @staticmethod
    def add_report_arguments(parser):
        parser.add_argument(
            "-p",
            "--pool",
            help="name of collector to query",
        )
        parser.add_argument(
            "-F",
            "--condor-history-file",
            metavar="FILE",
            help="read history data from specified file",
        )
        parser.add_argument(
            "-C",
            "--constraint",
            dest="constraints",
            action="append",
            default=[],
            help="extra constraint to add to history query, "
                 "can be given multiple times",
        )
