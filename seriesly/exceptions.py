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


class BadRequest(Exception):

    def __init__(self, err_message):
        self.err_message = err_message

    def __str__(self):
        return self.err_message


class BadResponse(Exception):

    def __init__(self, err_message):
        self.err_message = err_message

    def __str__(self):
        return self.err_message
