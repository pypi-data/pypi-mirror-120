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

"""Tests for the `igwn_accounting.batch.base` module
"""

__author__ = "Duncan Macleod <duncan.macleod@ligo.org>"

import argparse
from unittest import mock


class _TestBatchSystem():
    """Abstract test class for concrete instances of the BatchSystem
    """
    TEST_CLASS = None  # needs to be set by subclasses

    def test_system_info(self):
        with mock.patch.object(
                self.TEST_CLASS,
                "get_system_version",
                lambda: "mock",
        ):
            assert self.TEST_CLASS.system_info() == {
                "name": self.TEST_CLASS.name,
                "version": "mock",
            }

    def test_add_report_argument_group(self):
        parser = argparse.ArgumentParser()
        self.TEST_CLASS.add_report_argument_group(parser)
        assert [
            g for g in parser._action_groups
            if g.title == self.TEST_CLASS.name]
