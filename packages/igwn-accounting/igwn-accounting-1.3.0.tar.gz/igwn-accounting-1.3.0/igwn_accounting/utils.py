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

"""Generate a report of IGWN Computing Grid usage for a 24-hour period.
"""

import datetime
import logging
import sys

from dateutil.parser import parse as _parse_date
from dateutil import tz

__author__ = "Duncan Macleod <duncan.macleod@ligo.org>"

# date handling
UTC = tz.tzutc()


def datetime_from_epoch(dt, tzinfo=UTC):
    """Returns the `datetime.datetime` for a given Unix epoch

    Parameters
    ----------
    dt : `float`
        a Unix timestamp

    tzinfo : `datetime.tzinfo`, optional
        the desired timezone for the output `datetime.datetime`

    Returns
    -------
    datetime.datetime
        the datetime that represents the given Unix epoch
    """
    return datetime.datetime.utcfromtimestamp(dt).replace(tzinfo=tzinfo)


def parse_date(input_):
    try:
        return _parse_date(input_).replace(tzinfo=UTC)
    except ValueError as exc:
        try:
            input_ = float(input_)
        except (TypeError, ValueError):
            raise exc
        return datetime_from_epoch(input_)


def init_logging(name, stream=sys.stderr):
    logger = logging.getLogger(name)
    handler = logging.StreamHandler(stream)
    handler.setFormatter(logging.Formatter(
        '[%(name)s %(asctime)s] %(levelname)+8s: %(message)s',
    ))
    logger.addHandler(handler)
    return logger


DEFAULT_LOGGER = init_logging("igwn-accounting")
