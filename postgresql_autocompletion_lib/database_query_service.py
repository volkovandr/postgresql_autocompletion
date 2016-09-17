'''The database query service implements a set of functions that are used
to connect to a database and to query the database schema'''


class database_query_service:
    def connect(host, port, database, user, passswork):
        raise NotImplementedError()

    def getSchemas():
        raise NotImplementedError()

