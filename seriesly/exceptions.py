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
