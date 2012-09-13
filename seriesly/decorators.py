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
from functools import wraps

import requests

from seriesly.exceptions import BadResponse, ConnectionError, \
    NotExistingDatabase, ExistingDatabase


def formatter(method):
    """Check response status code and return response in appropriate format"""
    @wraps(method)
    def wrapper(*args, **kargs):
        response = method(*args, **kargs)

        if response.status_code != requests.codes.ok:
            raise BadResponse(response.text)

        frmt = kargs.get('frmt', None) or ('text' in args and 'text') or 'dict'
        if frmt == 'dict':
            return response.json
        else:
            return response.text
    return wrapper


def verbose_error(function):
    """Ensure more verbose error message in case of connection error"""
    @wraps(function)
    def wrapper(self, url, *args, **kargs):
        try:
            return function(self, url, *args, **kargs)
        except requests.exceptions.ConnectionError:
            raise ConnectionError(self.base_url)
    return wrapper


def only_existing(function):
    """Allow operations only on existing databases"""
    @wraps(function)
    def wrapper(self, dbname):
        if dbname not in self.list_dbs():
            raise NotExistingDatabase(dbname)
        else:
            return function(self, dbname)
    return wrapper


def only_not_existing(function):
    """Allow operations only on not existing databases."""
    @wraps(function)
    def wrapper(self, dbname):
        if dbname in self.list_dbs():
            raise ExistingDatabase(dbname)
        else:
            return function(self, dbname)
    return wrapper
