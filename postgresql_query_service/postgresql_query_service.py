if __package__ == 'postgresql_query_service':
    from postgresql_query_service import postgresql
    from postgresql_autocompletion_lib.database_query_service \
        import database_query_service
else:
    from ..postgresql_query_service import postgresql
    from ..postgresql_autocompletion_lib.database_query_service \
        import database_query_service


class postgresql_query_service(database_query_service):

    def __init__(self):
        self.connection = None

    def connect(self, host, port, database, user, password):
        self.connection = postgresql.open(
            user=user,
            host=host,
            port=port,
            database=database,
            password=password)

    def getSchemas(self):
        if self.connection is None:
            raise Exception("Not connected to the database")
        return [
            row[0] for row in
            self.connection.query('''
                SELECT schema_name
                    FROM information_schema.schemata
                    ORDER BY schema_name''')]

    def isConnected(self):
        if not self.connection:
            return False
        try:
            self.connection.query("SELECT 1")
            return True
        except:
            return False
