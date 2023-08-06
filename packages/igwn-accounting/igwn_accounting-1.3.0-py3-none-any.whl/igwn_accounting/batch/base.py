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

"""Base implementation of BatchSystem interface
"""

from abc import (
    ABC,
    abstractmethod,
)


class BatchSystem(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @classmethod
    def system_info(cls):
        return {
            "name": cls.name,
            "version": cls.get_system_version(),
        }

    @staticmethod
    @abstractmethod
    def get_system_version():
        pass

    @staticmethod
    @abstractmethod
    def get_jobs(
        start,
        end,
        schedulers=None,
        parallel=1,
        **kwargs
    ):
        pass

    @classmethod
    @abstractmethod
    def add_report_argument_group(cls, parser):
        group = parser.add_argument_group(
            title=cls.name,
            description=(
                "Options for the querying the {} batch system".format(cls.name)
            ),
        )
        return cls.add_report_arguments(group)

    @staticmethod
    @abstractmethod
    def add_report_arguments(parser):
        pass
