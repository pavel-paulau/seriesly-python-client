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

from seriesly.exceptions import BadRequest
from seriesly.decorators import verbose_error, only_existing, \
    only_not_existing, formatter


class HttpClient(object):

    """HTTP client with base URL
    """

    def __init__(self, host='127.0.0.1', port=3133):
        """Initialize base URL.

        :param host: hostname or IP address
        :param port: port
        """
        self.base_url = 'http://{0}:{1}/'.format(host, port)

    @verbose_error
    def _get(self, url, params=None):
        """Send GET request and return the response object.

        :param url: request URL
        :param params: request params
        """
        return requests.get(url=self.base_url + url, params=params)

    @verbose_error
    def _post(self, url, data=None, params=None):
        """Send POST request and return the response object.

        :param url: request URL
        :param data: request data
        :param params: request params
        """
        return requests.post(url=self.base_url + url, data=data, params=params)

    @verbose_error
    def _put(self, url):
        """Send PUT request and return the response object.

        :param url: request URL
        """
        return requests.put(url=self.base_url + url)

    @verbose_error
    def _delete(self, url):
        """Send DELETE request and return the response object.

        :param url: request URL
        """
        return requests.delete(url=self.base_url + url)


class Seriesly(HttpClient):

    """seriesly connection and database manager
    """

    @only_not_existing
    def create_db(self, dbname):
        """Create the 'dbname' database.

        :param dbname: database name
        """
        self._put(dbname)

    def list_dbs(self):
        """Return a list of all known database names on the server"""
        return self._get('_all_dbs').json

    @only_existing
    def drop_db(self, dbname):
        """Delete the 'dbname' database.

        :param dbname: database name
        """
        self._delete(dbname)

    @only_existing
    def __getattr__(self, dbname):
        """Return an instance of the Database class.

        :param dbname: database name
        """
        return self.__getitem__(dbname)

    @only_existing
    def __getitem__(self, dbname):
        """Return an instance of the Database class.

        :param dbname: database name
        """
        return Database(dbname=dbname, connection=self)


class Database(object):

    """Datastore
    """

    def __init__(self, dbname, connection):
        self._dbname = dbname
        self._connection = connection

    def append(self, data, timestamp=None):
        """Store a JSON document with a system-generated or user-specified
        timestamps.
        Return a response body as string.

        :param data: arbitrary data dictionary
        :param timestamp: user-specified timestamp in one of supported format
        """
        if not isinstance(data, dict) or not data:
            raise BadRequest('Non-empty dictionary is expected')

        params = timestamp and {'ts': timestamp} or {}
        response = self._connection._post(self._dbname,
                                          json.dumps(data),
                                          params)
        return response.text

    @formatter
    def query(self, params, frmt='dict'):
        """Querying data in seriesly database.
        Return a response body as string or dictionary.

        :param params: dictionary with query parameters (only 'to', 'from',   \
        'group', 'ptr' and 'reducer' are supported so far). The dictionary    \
        values can be lists for representing multivalued query parameters.
        :param frmt: format of query response, 'text' or 'dict'
        """
        if not isinstance(params, dict) or not params:
            raise BadRequest('Non-empty dictionary is expected')
        for param in params:
            if param not in ('to', 'from', 'group', 'ptr', 'reducer'):
                raise BadRequest('Unexpected parameter "{0}"'.format(param))

        return self._connection._get(self._dbname + '/_query', params)

    @formatter
    def get_one(self, timestamp, frmt='dict'):
        """Retrieve individual document from database.
        Return a response body as string or dictionary.

        :param timestamp: timestamp of document.
        :param frmt: format of response, 'text' or 'dict'
        """
        return self._connection._get(self._dbname + '/' + timestamp)

    @formatter
    def get_all(self, frmt='dict'):
        """Retrieve all documents from database.
        Return a response body as string or dictionary.

        :param frmt: format of response, 'text' or 'dict'
        """
        return self._connection._get(self._dbname + '/_all')
