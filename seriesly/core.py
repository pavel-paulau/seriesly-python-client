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
import json

import requests

from exceptions import verbose_error, only_existing, only_not_existing, \
    correct_data, correct_params, BadResponse


class HttpClient(object):

    """HTTP client with base URL
    """

    def __init__(self, host='127.0.0.1', port=3133):
        """Initialize base URL"""
        self.base_url = 'http://{0}:{1}/'.format(host, port)

    @verbose_error
    def get(self, url, params=None):
        """Send GET request and return the response object"""
        return requests.get(url=self.base_url + url, params=params)

    @verbose_error
    def post(self, url, data=None, params=None):
        """Send POST request and return the response object"""
        return requests.post(url=self.base_url + url, data=data, params=params)

    @verbose_error
    def put(self, url):
        """Send PUT request and return the response object"""
        return requests.put(url=self.base_url + url)

    @verbose_error
    def delete(self, url):
        """Send DELETE request and return the response object"""
        return requests.delete(url=self.base_url + url)


class Seriesly(HttpClient):

    """seriesly connection and database manager
    """

    @only_not_existing
    def create_db(self, dbname):
        """Create the `dbname` database"""
        self.put(dbname)

    def list_dbs(self):
        """List all known databases on the server"""
        return self.get('_all_dbs').json

    @only_existing
    def drop_db(self, dbname):
        """Delete the `dbname` database."""
        self.delete(dbname)

    @only_existing
    def __getattr__(self, dbname):
        """Return an instance of the Database class"""
        return self.__getitem__(dbname)

    @only_existing
    def __getitem__(self, dbname):
        """Return an instance of the Database class"""
        return Database(dbname=dbname, connection=self)


class Database(object):

    """Datastore
    """

    def __init__(self, dbname, connection):
        self.dbname = dbname
        self.connection = connection

    @correct_data
    def append(self, data, timestamp=None):
        """Store a JSON document with a system-generated or user-specified
        timestamps"""
        params = timestamp and {'ts': timestamp} or {}
        return self.connection.post(self.dbname, json.dumps(data), params).text

    @correct_params
    def query(self, params=None, format='json'):
        """Querying data in seriesly database"""
        params = params or {}
        response = self.connection.get(self.dbname + '/_query', params)
        if response.status_code != requests.codes.ok:
            raise BadResponse(response.text)

        if format == 'json':
            return response.json
        else:
            return response.text
