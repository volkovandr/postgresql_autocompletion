'''Implements a mocker class for database query service
Used in unit tests'''


from postgresql_autocompletion_lib.database_query_service \
    import database_query_service


class dbmocker_query_service(database_query_service):

    def connect(self, host, port, database, user, passsword):
        pass

    def getSchemas(self):
        return ["public", "test_schema1"]
