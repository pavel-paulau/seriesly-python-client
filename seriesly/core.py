import requests
import ujson as json

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
        return self._get('_all_dbs').json()

    @only_existing
    def drop_db(self, dbname):
        """Delete the 'dbname' database.

        :param dbname: database name
        """
        self._delete(dbname)

    def __getattr__(self, dbname):
        """Return an instance of the Database class.

        :param dbname: database name
        """
        if dbname == "__name__":
            return super(Seriesly, self).__name__
        else:
            return self.__getitem__(dbname)

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

        url = self._dbname
        params = timestamp and {'ts': timestamp} or {}
        return self._connection._post(url, json.dumps(data), params).text

    @formatter
    def query(self, params, frmt='dict'):
        """Querying data in seriesly database.
        Return a response body as string or dictionary.

        :param params: dictionary with query parameters (only 'to', 'from',   \
        'group', 'ptr' and 'reducer', 'f' and 'fv' are supported so far). The \
        dictionary values can be lists for representing multivalued query     \
        parameters.
        :param frmt: format of query response, 'text' or 'dict'
        """
        if not isinstance(params, dict) or not params:
            raise BadRequest('Non-empty dictionary is expected')

        url = self._dbname + '/_query'
        return self._connection._get(url, params)

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
        url = self._dbname + '/_all'
        return self._connection._get(url)
