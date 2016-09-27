from postgresql_query_service import postgresql
from postgresql_autocompletion_lib.database_query_service \
    import database_query_service


class postgresql_query_service(database_query_service):

    def connect(self, host, port, database, user, password):
        self.connection = postgresql.open(
            user=user,
            host=host,
            port=port,
            database=database,
            password=password)

    def getSchemas(self):
        raise NotImplementedError()
