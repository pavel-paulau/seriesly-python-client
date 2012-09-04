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


class ConnectionError(Exception):

    def __init__(self, base_url):
        self.base_url = base_url

    def __str__(self):
        return 'Connection refused to "{0}"'.format(self.base_url)


class NotExistingDatabase(Exception):

    def __init__(self, dbname):
        self.dbname = dbname

    def __str__(self):
        return 'Database "{0}" does not exist'.format(self.dbname)


class ExistingDatabase(Exception):

    def __init__(self, dbname):
        self.dbname = dbname

    def __str__(self):
        return 'Database "{0}" already exists'.format(self.dbname)


class BadResponse(Exception):

    def __init__(self, err_message):
        self.err_message = err_message

    def __str__(self):
        return self.err_message
