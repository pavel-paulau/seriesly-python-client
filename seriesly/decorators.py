#
# Copyright 2012, Couchbase, Inc.
# All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License")
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
#
from decorator import decorator

import requests

from seriesly.exceptions import BadResponse, ConnectionError, \
    NotExistingDatabase, ExistingDatabase


@decorator
def formatter(method, *args, **kargs):
    """Check response status code and return response in appropriate format"""
    response = method(*args, **kargs)

    if response.status_code != requests.codes.ok:
        raise BadResponse(response.text)

    frmt = kargs.get('frmt', None) or ('text' in args and 'text') or 'dict'
    if frmt == 'dict':
        return response.json
    else:
        return response.text


@decorator
def verbose_error(method, self, *args, **kargs):
    """Ensure more verbose error message in case of connection error"""
    try:
        return method(self, *args, **kargs)
    except requests.exceptions.ConnectionError:
        raise ConnectionError(self.base_url)


@decorator
def only_existing(method, self, dbname):
    """Allow operations only on existing databases"""
    if dbname not in self.list_dbs():
        raise NotExistingDatabase(dbname)
    else:
        return method(self, dbname)


@decorator
def only_not_existing(method, self, dbname):
    """Allow operations only on not existing databases."""
    if dbname in self.list_dbs():
        raise ExistingDatabase(dbname)
    else:
        return method(self, dbname)
