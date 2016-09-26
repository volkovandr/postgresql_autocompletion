import postgresql_query_service.postgresql
from postgresql_autocompletion_lib.database_query_service \
    import database_query_service


class postgresql_query_service(database_query_service):

    def connect(self, host, port, database, user, passsword):
        raise NotImplementedError()

    def getSchemas(self):
        raise NotImplementedError()
