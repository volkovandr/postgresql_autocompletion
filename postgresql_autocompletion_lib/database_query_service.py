'''The database query service implements a set of functions that are used
to connect to a database and to query the database schema'''


class database_query_service:
    def connect(self, host, port, database, user, password):
        raise NotImplementedError()

    def getSchemas(self):
        raise NotImplementedError()
