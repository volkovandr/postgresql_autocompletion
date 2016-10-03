'''Implements a mocker class for database query service
Used in unit tests'''


from postgresql_autocompletion_lib.database_query_service \
    import database_query_service


class dbmocker_query_service(database_query_service):

    def __init__(self):
        self.connected = False

    def connect(self, host, port, database, user, password):
        self.connected = True
        pass

    def isConnected(self):
        return self.connected

    def getSchemas(self):
        return [
            "information_schema",
            "pg_catalog",
            "public",
            "test_schema",
            "test_schema2"]

    def getTables(self, schema_name=None):
        if schema_name is None:
            return [("test1_public", "public"), ("test2_public", "public")]
        if schema_name == "test_schema":
            return [
                ("table1_test1", "test_schema"),
                ("table2_test1", "test_schema")]

