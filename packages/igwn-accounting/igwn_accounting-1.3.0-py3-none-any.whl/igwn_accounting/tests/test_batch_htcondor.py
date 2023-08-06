# -*- coding: utf-8 -*-
# Copyright 2021-2021 Cardiff University
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

"""Tests for the `igwn_accounting.batch.htcondor` module
"""

__author__ = "Duncan Macleod <duncan.macleod@ligo.org>"

import subprocess
from pathlib import Path
from shutil import which
from unittest import mock

import pytest

from .. import (
    report as igwn_report,
)
from ..batch import htcondor as batch_htcondor
from . import utils
from .test_batch_base import _TestBatchSystem

# -- test data --------------

DATA_FILE = Path(__file__).parent / "condor_history.txt"
RESULT_ASCII = """
user1 tag1 7 2021-01-01 OSG.Remote
user1 tag1 7 2021-01-01 TEST
user1 tag2 2 2021-01-01 OSG.Remote
user2 tag1 2 2021-01-01 OSG.Remote
user2 tag1 2 2021-01-01 TEST
""".strip()


@pytest.fixture
def condor_history_file(tmpdir):
    history_file = str(tmpdir.join("history.txt"))
    with open(history_file, "w") as hf:
        utils.history_from_jsonl(str(DATA_FILE), hf)
    return history_file


# -- unit tests ---------------------------------

MOCK_CONDOR_VERSION_OUTPUT = """
$CondorVersion: 8.8.5 Sep 04 2019 BuildID: 480168 PackageID: 8.8.5-1 $
$CondorPlatform: x86_64_RedHat7 $
""".strip()


@mock.patch(
    "subprocess.check_output",
    return_value=MOCK_CONDOR_VERSION_OUTPUT.encode("utf-8"),
)
def test_get_condor_version(mock):
    assert batch_htcondor.get_condor_version(executable="mock") == (
        MOCK_CONDOR_VERSION_OUTPUT
    )


@pytest.mark.parametrize(("mockoutput", "version"), [
    (b"$CondorVersion: 8.8.5 Sep 04 2019 4.5.6\nsomething else 1.2.3",
     "8.8.5"),
    (b"8.8.5 condor something", "8.8.5"),
    (b"HTCondor 10.11.123rc1", "10.11.123rc1"),
])
@mock.patch("subprocess.check_output")
def test_get_condor_version_number(mock, mockoutput, version):
    mock.return_value = mockoutput
    assert batch_htcondor.get_condor_version_number(
        executable="mock",
    ) == version


@pytest.mark.parametrize("userad, tagad", [
    (batch_htcondor.IGWN_USER_CLASSAD, batch_htcondor.IGWN_TAG_CLASSAD),
    ("Owner", "AccountingGroup"),
])
def test_parse_job(userad, tagad):
    job = {
        userad: "test",
        tagad: "test.dev.pytest",
        "MaxHosts": 2,
        "RequestCpus": 2,
        "RemoteWallClockTime": 100.,
        "CompletionDate": 1609460000,
        "CumulativeSuspensionTime": 10.,
    }
    assert batch_htcondor.parse_job(job, "deepthought") == (
         "test",
         "test.dev.pytest",
         (100. - 10.) * 2 * 2 / 3600.,
         "2021-01-01",
         "deepthought",
    )


@pytest.mark.parametrize("glidein_site, jobcluster", [
    # job that didn't report 'Site'
    (None, "deepthought"),
    # distributed job that reported as a local job
    ("Unknown", "deepthought"),
    # distributed job that ran remotely
    ("REMOTE", "OSG.REMOTE"),
])
def test_parse_job_osg(glidein_site, jobcluster):
    job = {
        batch_htcondor.IGWN_USER_CLASSAD: "test",
        batch_htcondor.IGWN_TAG_CLASSAD: "test.dev.pytest",
        "CompletionDate": 0,
        "CumulativeSuspensionTime": 0.,
        "EnteredCurrentStatus": 1609460000,
        "MATCH_GLIDEIN_Site": glidein_site,
        "RemoteWallClockTime": 3600.,
    }
    assert batch_htcondor.parse_job(job, "deepthought") == (
         "test",
         "test.dev.pytest",
         1.,
         "2021-01-01",
         jobcluster,
    )


@mock.patch("socket.getfqdn")
@mock.patch("shutil.which", return_value="/test/condor_history")
@mock.patch("subprocess.run")
@pytest.mark.parametrize("fqdn", ["sched.test", "sched2.test"])
def test_get_history_subprocess_call(sprun, _, getfqdn, fqdn):
    # configure getfqdn mock
    getfqdn.return_value = fqdn

    # run the subprocess function
    batch_htcondor._get_history_subprocess(
        "sched.test",
        "Owner == test",
        ["A", "B"],
        "ClassAd > 12345",
        "pool.test",
    )

    expected = [
        "/test/condor_history",
        "-since", "ClassAD > 12345",
        "-constraint", "Owner == test",
        "-pool", "pool.test",
        "-af", "A", "B",
    ]
    if fqdn == "sched.test":  # -name is only used if necessary
        expected = expected[:5] + ["-name", "sched.test"] + expected[5:]

    assert sprun.called_once_with(
        expected,
        stdout=subprocess.PIPE,
        check=True,
    )


class TestHTCondor(_TestBatchSystem):
    TEST_CLASS = batch_htcondor.HTCondor

    @mock.patch(
        "subprocess.check_output",
        return_value=MOCK_CONDOR_VERSION_OUTPUT.encode("utf-8"),
    )
    def test_get_system_version(self, mock):
        assert (
            self.TEST_CLASS.get_system_version()
            == MOCK_CONDOR_VERSION_OUTPUT
        )


# -- integration tests --------------------------


@pytest.mark.skipif(
    which("condor_history") is None,
    reason="no condor_history exe",
)
@mock.patch(
    "igwn_accounting.report.get_run_metadata",
    return_value={"key": "value"},
)
def test_main_condor_history_file(_, tmpdir, condor_history_file):
    """Check that the whole thing works with --condor-history-file

    This allows a fairly robust check of the full system, including
    a real-world test of the _get_history_subprocess function
    """
    output = tmpdir.join("output.txt")
    igwn_report.main([
        "--batch-system", "htcondor",
        "--cluster", "TEST",
        "--scheduler", "test.sched",
        "--utc", "2021-01-01",
        "--output-file", str(output),
        "--format", "ascii",
        "--condor-history-file", str(condor_history_file),
    ])
    assert output.read().strip() == RESULT_ASCII
