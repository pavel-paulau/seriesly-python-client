import requests
import json

from seriesly.exceptions import BadRequest, NotExistingDatabase, \
    ExistingDatabase
from seriesly.decorators import verbose_error


class HttpClient(object):

    """HTTP client with base URL
    """

    def __init__(self, host='127.0.0.1', port=3133):
        """Initialize base URL.

        :param host: hostname or IP address
        :param port: port
        """
        self.base_url = 'http://{0}:{1}/'.format(host, port)
        self.session = requests.Session()

    @verbose_error
    def get(self, url, params=None):
        """Send GET request and return the response object.

        :param url: request URL
        :param params: request params
        """
        return self.session.get(url=self.base_url + url, params=params)

    @verbose_error
    def post(self, url, data=None, params=None):
        """Send POST request and return the response object.

        :param url: request URL
        :param data: request data
        :param params: request params
        """
        return self.session.post(url=self.base_url + url, data=data, params=params)

    @verbose_error
    def put(self, url):
        """Send PUT request and return the response object.

        :param url: request URL
        """
        return self.session.put(url=self.base_url + url)

    @verbose_error
    def delete(self, url):
        """Send DELETE request and return the response object.

        :param url: request URL
        """
        return self.session.delete(url=self.base_url + url)


class Seriesly(HttpClient):

    """seriesly connection and database manager
    """

    def create_db(self, dbname):
        """Create the 'dbname' database.

        :param dbname: database name
        """
        if dbname not in self.list_dbs():
            return self.put(dbname).text
        else:
            raise ExistingDatabase(dbname)

    def list_dbs(self):
        """Return a list of all known database names on the server"""
        return self.get('_all_dbs').json()

    def drop_db(self, dbname):
        """Delete the 'dbname' database.

        :param dbname: database name
        """
        if dbname in self.list_dbs():
            return self.delete(dbname).text
        else:
            raise NotExistingDatabase(dbname)

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
        timestamps. Return a response body as string.

        :param data: arbitrary data dictionary
        :param timestamp: user-specified timestamp in one of supported format
        """
        if not isinstance(data, dict) or not data:
            raise BadRequest('Non-empty dictionary is expected')

        url = self._dbname
        params = timestamp and {'ts': timestamp} or {}
        return self._connection.post(url, json.dumps(data), params).text

    def query(self, params):
        """Querying data in seriesly database.
        Return a response body as dictionary.

        :param params: dictionary with query parameters. The dictionary values \
        can be lists for representing multivalued query parameters.
        """
        if not isinstance(params, dict) or not params:
            raise BadRequest('Non-empty dictionary is expected')

        url = self._dbname + '/_query'
        return self._connection.get(url, params).json()

    def get_one(self, timestamp):
        """Retrieve individual document from database.
        Return a response body as dictionary.

        :param timestamp: timestamp of document.
        """
        return self._connection.get(self._dbname + '/' + timestamp).json()

    def get_all(self):
        """Retrieve all documents from database.
        Return a response body as dictionary.
        """
        url = self._dbname + '/_all'
        return self._connection.get(url).json()

    def compact(self):
        """Trigger online database compactions
        """
        url = self._dbname + '/_compact'
        return self._connection.post(url).json()
