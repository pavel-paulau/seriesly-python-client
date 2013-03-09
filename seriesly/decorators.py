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
        return response.json()
    else:
        return response.text


@decorator
def verbose_error(method, self, *args, **kargs):
    """Ensure more verbose error message in case of connection error"""
    try:
        response = method(self, *args, **kargs)
        if response.status_code == 500:
            raise Exception(response.text)
        else:
            return response
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
