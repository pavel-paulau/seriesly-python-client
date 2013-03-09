from decorator import decorator

import requests

from seriesly.exceptions import ConnectionError, BadRequest


@decorator
def verbose_error(method, self, *args, **kargs):
    """Ensure more verbose error message in case of connection error"""
    try:
        response = method(self, *args, **kargs)
        if response.status_code >= 400:
            raise BadRequest(response.text)
        else:
            return response
    except requests.exceptions.ConnectionError:
        raise ConnectionError(self.base_url)
