import time

from decorator import decorator
from requests.exceptions import ConnectionError

from seriesly.exceptions import ConnectionError as _ConnectionError, BadRequest


MAX_RETRY = 5
RETRY_DELAY = 5


@decorator
def handle_error(method, self, *args, **kargs):
    """Gracefully handle request errors"""
    error = ''
    for _ in range(MAX_RETRY):
        try:
            response = method(self, *args, **kargs)
        except ConnectionError as e:
            error = e
            time.sleep(RETRY_DELAY)
            continue
        else:
            if response.status_code >= 400:
                raise BadRequest(response.text)
            else:
                return response
    raise _ConnectionError(error)
