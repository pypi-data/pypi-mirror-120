# -*- coding: utf-8 -*-
# Copyright 2020 Cardiff University
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

"""Generate a report of IGWN Computing Grid usage for a 24-hour period.
"""

import argparse
import datetime
import json
import logging
import sys
from collections import defaultdict
from getpass import getuser
from math import ceil
from socket import getfqdn

from dateutil import tz

from . import __version__
from .batch import BATCH_SYSTEMS
from .utils import (
    DEFAULT_LOGGER as LOGGER,
    datetime_from_epoch,
    parse_date,
)

__author__ = "Duncan Macleod <duncan.macleod@ligo.org>"

PROG = "igwn-accounting-report"

# date handling
UTC = tz.tzutc()
LOCAL = tz.tzlocal()
NOW = datetime.datetime.utcnow().replace(
    microsecond=0,
    tzinfo=UTC,
)
TODAY = NOW.replace(hour=0, minute=0, second=0)
YESTERDAY = TODAY + datetime.timedelta(days=-1)


# -- utilities --------------

def find_epoch(utcstart, days=1, **delta):
    """Returns the Unix epoch [start, end) interval for the given UTC day

    Parameters
    ----------
    utcstart : `datetime.datetime`
        the UTC start datetime of the interval

    days, **delta
        duration of interval expressed as keyword arguments to
        :class:`datetime.timedelta`

    Returns
    -------
    utcstart, utcend : `float`
        a pair of Unix epoch floats that define the interval
    """
    utcend = utcstart + datetime.timedelta(days=days, **delta)
    return utcstart.timestamp(), utcend.timestamp()


# -- command-line parsing ---

class HelpFormatter(
    argparse.ArgumentDefaultsHelpFormatter,
    argparse.RawDescriptionHelpFormatter,
):
    """Help formatter with customisations to support argparse-manpage
    """
    def _format_usage(self, usage, actions, groups, prefix):
        if prefix is None:
            prefix = "Usage: "
        return super()._format_usage(
            usage,
            actions,
            groups,
            prefix,
        )


class ArgumentParser(argparse.ArgumentParser):
    """`ArgumentParser` with customisations to support argparse-manpage
    """
    def __init__(self, *args, **kwargs):
        manpage = kwargs.pop("manpage", None)

        kwargs.setdefault("description", __doc__)
        kwargs.setdefault("formatter_class", HelpFormatter)
        super(ArgumentParser, self).__init__(*args, **kwargs)

        self._positionals.title = "Required arguments"
        self._optionals.title = "Options"

        # add manpage options for argparse-manpage
        self._manpage = manpage

    def get_batch_kwargs(self, args):
        batch_group, = list(filter(
            lambda x: x.title.lower() == args.batch_system,
            self._action_groups,
        ))
        return {
            a.dest: getattr(args, a.dest) for a in batch_group._group_actions
            if hasattr(args, a.dest)
        }


def create_parser():
    """Create a command-line parser for this tool
    """
    parser = ArgumentParser(prog=PROG)
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="show verbose output",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=__version__,
        help="show version number and exit",
    )
    parser.add_argument(
        "-c",
        "--cluster",
        required=True,
        help="computing centre from which the accounting data comes "
             "(required)",
    )
    parser.add_argument(
        "-b",
        "--batch-system",
        default="htcondor",
        choices=list(BATCH_SYSTEMS.keys()),
        help="batch system to query",
    )
    parser.add_argument(
        "-s",
        "--schedulers",
        "--partitions",
        nargs="*",
        help="schedulers/partitions to query, multiple arguments can be given",
    )
    dategroup = parser.add_mutually_exclusive_group()
    dategroup.add_argument(
        "-u",
        "--utc",
        default=YESTERDAY,
        type=parse_date,
        help="UTC date to query",
    )
    dategroup.add_argument(
        "-t",
        "--epoch",
        nargs=2,
        metavar=("START", "END"),
        type=parse_date,
        help="start and end datetimes or Unix epochs to query; "
             "NOTE: these times should form a semi-open interval "
             "[START,END)",
    )
    parser.add_argument(
        "-o",
        "--output-file",
        default="stdout",
        help="path of file to write output into",
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=("json", "ascii"),
        default="ascii",
        help="output format",
    )
    parser.add_argument(
        "-j",
        "--jobs",
        type=int,
        default=1,
        help="number of processes to use",
    )
    parser.add_argument(
        "-w",
        "--warn-on-error",
        action="store_true",
        default=False,
        help="only print a warning when history queries fail "
             "rather than erroring",
    )

    # add custom options for each batch system
    for system in BATCH_SYSTEMS.values():
        system.add_report_argument_group(parser)

    # augment parser for argparse-manpage
    parser.man_short_description = "generate a batch system usage report"

    return parser


def get_run_metadata(batchinfo):
    """Returns a `dict` of useful metadata regarding this process

    Mainly for debugging issues with the data.
    """
    return {
        "collector_name": "igwn-accounting-report",
        "collector_version": __version__,
        "python_version": sys.version,
        "batch_system": batchinfo,
        "host": getfqdn(),
        "user": getuser(),
        "utcdate": str(datetime.datetime.utcnow()),
        "cmd": " ".join(sys.argv),
    }


def print_ascii(data, file):
    for key in sorted(data):
        owner, tag, date, jobcluster = key
        print(
            "{} {} {} {} {}".format(
                owner,
                tag,
                ceil(data[key]),
                date,
                jobcluster,
            ),
            file=file,
        )


def print_json(data, meta, file):
    reformatted = []
    for key in sorted(data):
        owner, tag, date, jobcluster = key
        reformatted.append({
            "user": owner,
            "tag": tag,
            "resource": jobcluster,
            "utcdate": date,
            "usage": ceil(data[key]),
        })

    jdata = {
        "data": reformatted,
        "meta": meta,
    }

    json.dump(
        jdata,
        file,
        indent=None,
        separators=(",", ":"),
        sort_keys=True,
    )


def main(args=None):
    """Run the thing

    Parameters
    ----------
    args : `list`
        the input command line arguments, defaults to `sys.argv`
    """
    parser = create_parser()
    args = parser.parse_args(args=args)
    batchkw = parser.get_batch_kwargs(args)

    if args.verbose:
        LOGGER.setLevel(logging.DEBUG)

    # finalise epoch to query
    if args.epoch:
        startutc, endutc = args.epoch
        start = datetime.datetime.timestamp(startutc)
        end = datetime.datetime.timestamp(endutc)
    else:  # args.utc
        start, end = find_epoch(args.utc)
        startutc = datetime_from_epoch(start)
        endutc = datetime_from_epoch(end)
    LOGGER.info("Now: {} | {}".format(NOW, NOW.astimezone(LOCAL)))
    LOGGER.info(
        "Epoch start: {} | {} | {}".format(
            start,
            startutc,
            startutc.astimezone(LOCAL)
        ),
    )
    LOGGER.info(
        "Epoch end:   {} | {} | {}".format(
            end,
            endutc,
            endutc.astimezone(LOCAL)
        ),
    )

    accounting = defaultdict(int)
    cluster = args.cluster

    # parse the batch system
    batch_system = BATCH_SYSTEMS["htcondor"]

    # get history from the batch system
    history = batch_system.get_jobs(
        start,
        end,
        args.schedulers,
        cluster=cluster,
        error=not args.warn_on_error,
        parallel=args.jobs,
        **batchkw,
    )

    # total jobs by owner, tag, and location
    for i, (owner, tag, cost, date, jobcluster) in enumerate(history):
        accounting[(owner, tag, date, jobcluster)] += cost
    try:
        LOGGER.info("Parsed {} jobs".format(i+1))
    except UnboundLocalError:
        LOGGER.warning("Parsed 0 jobs")

    # get run metadata
    runinfo = get_run_metadata(batch_system.system_info())

    # write output
    LOGGER.info("Writing output")
    if args.output_file == "stdout":
        file = sys.stdout
    else:
        file = open(args.output_file, "w")
    try:
        if args.format == "ascii":
            print_ascii(accounting, file)
        elif args.format == "json":
            print_json(accounting, runinfo, file)
            if file is sys.stdout:  # json doesn't print trailing newline
                print()
    finally:
        # close the output file
        if file is not sys.stdout:
            file.close()
            LOGGER.debug("Output written to {}".format(args.output_file))


# execute the module (enables running as `python -m igwn_accounting.report`)
if __name__ == "__main__":
    main()
