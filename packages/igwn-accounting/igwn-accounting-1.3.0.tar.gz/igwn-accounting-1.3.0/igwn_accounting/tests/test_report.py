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

"""Tests for the `igwn_accounting.report` module
"""

__author__ = "Duncan Macleod <duncan.macleod@ligo.org>"

import json
import sys
from getpass import getuser
from pathlib import Path
from socket import getfqdn
from unittest import mock

import pytest

from .. import report as igwn_report
from . import utils

# -- test data --------------

DATA_FILE = Path(__file__).parent / "condor_history.txt"
RESULT_JSON = json.dumps({
    "data": [
        {"user": "user1", "tag": "tag1", "usage": 7,
         "utcdate": "2021-01-01", "resource": "OSG.Remote"},
        {"user": "user1", "tag": "tag1", "usage": 7,
         "utcdate": "2021-01-01", "resource": "TEST"},
        {"user": "user1", "tag": "tag2", "usage": 2,
         "utcdate": "2021-01-01", "resource": "OSG.Remote"},
        {"user": "user2", "tag": "tag1", "usage": 2,
         "utcdate": "2021-01-01", "resource": "OSG.Remote"},
        {"user": "user2", "tag": "tag1", "usage": 2,
         "utcdate": "2021-01-01", "resource": "TEST"},
    ],
    "meta": {
        "key": "value",
    },
}, indent=None, sort_keys=True, separators=(",", ":"))
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


# -- tests ------------------

@mock.patch("subprocess.check_output", return_value=b"condor version 1.2.3")
@mock.patch.object(sys, "argv", ["a", "b", "c"])
@mock.patch.object(Path, "exists")
@mock.patch("datetime.datetime")
@pytest.mark.parametrize("has_condor_version, condor_version", [
    (False, None),
    (True, "condor version 1.2.3"),
])
def test_get_run_metadata(
        mock_datetime,
        mock_path_exists,
        mock_sys_argv,
        has_condor_version,
        condor_version,
):
    # finalise mocks
    mock_datetime.utcnow.return_value = "some date"
    mock_path_exists.return_value = has_condor_version

    # fake batch info (doesn't do anything)
    batchinfo = "blah"

    # check function formats data correctly
    assert igwn_report.get_run_metadata(batchinfo) == {
        "collector_name": "igwn-accounting-report",
        "collector_version": igwn_report.__version__,
        "batch_system": batchinfo,
        "user": getuser(),
        "host": getfqdn(),
        "python_version": sys.version,
        "cmd": "a b c",
        "utcdate": "some date",
    }


# end-to-end test with fake data


def mock_get_history(*args, **kwargs):
    with DATA_FILE.open("r") as file:
        for line in file:
            yield json.loads(line)


@pytest.mark.parametrize("fmt, expected", (
    ("ascii", RESULT_ASCII),
    ("json", RESULT_JSON),
))
@mock.patch(
    "igwn_accounting.batch.htcondor._get_history_python",
    mock_get_history,
)
@mock.patch(
    "igwn_accounting.report.get_run_metadata",
    lambda x: {"key": "value"},
)
@mock.patch(
    "igwn_accounting.batch.htcondor.get_condor_version",
    return_value="mock",
)
def test_main(_, fmt, expected, tmpdir):
    output = tmpdir.join("output.txt")
    igwn_report.main([
        "--batch-system", "htcondor",
        "--cluster", "TEST",
        "--scheduler", "test.sched",
        "--utc", "2021-01-01",
        "--output-file", str(output),
        "--format", fmt,
    ])
    # check output matches
    assert output.read().strip() == expected
