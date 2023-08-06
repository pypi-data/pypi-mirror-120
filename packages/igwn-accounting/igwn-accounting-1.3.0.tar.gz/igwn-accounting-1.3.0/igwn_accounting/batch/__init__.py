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

"""Batch system interfaces for the IGWN Accounting system

To implement a new batch system:

1. create a new module under igwn_accounting/batch/ that
   implements a concrete instance of the `BatchSystem` abstract
   class, particularly the `get_jobs` and `get_system_version`
   methods,

2. add the new module to the ``from . import ...` statement
   below.
"""

from .base import BatchSystem

# supported batch systems
from . import (
    htcondor,
)

BATCH_SYSTEMS = {x.name.lower(): x for x in BatchSystem.__subclasses__()}
