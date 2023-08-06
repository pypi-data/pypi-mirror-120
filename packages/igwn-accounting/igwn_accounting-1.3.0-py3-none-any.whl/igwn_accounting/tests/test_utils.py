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

"""Tests for the `igwn_accounting.utils` module
"""

__author__ = "Duncan Macleod <duncan.macleod@ligo.org>"

import datetime
import logging

from dateutil import tz

import pytest

from .. import utils as igwn_utils


@pytest.mark.parametrize("in_, out", (
    ("2021-01-01", datetime.datetime(2021, 1, 1, tzinfo=tz.tzutc())),
    ("1609459200.0", datetime.datetime(2021, 1, 1, tzinfo=tz.tzutc())),
))
def test_parse_date(in_, out):
    assert igwn_utils.parse_date(in_) == out


def test_parse_date_error():
    with pytest.raises(ValueError) as exc:
        igwn_utils.parse_date("bad")
    assert str(exc.value.args[0]).startswith("Unknown string format")


def test_init_logging():
    logger = igwn_utils.init_logging("test")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test"
