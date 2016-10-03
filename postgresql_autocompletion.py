'''This is the main module for Sublime plugin PostgeSQL autocompletion'''

try:
    import sublime
    import sublime_plugin
except ImportError:
    import sublime_mocker
    import sublime_plugin_mocker
    sublime = sublime_mocker
    sublime_plugin = sublime_plugin_mocker

if __package__:
    from .postgresql_query_service.postgresql_query_service \
        import postgresql_query_service
    from .postgresql_autocompletion_lib.helpers \
        import checkSyntax, getQueryText, getSettings
    from .postgresql_autocompletion_lib.sqlparser import base_parse, \
        cursorPositionInQuery, parseFrom
else:
    from postgresql_query_service.postgresql_query_service \
        import postgresql_query_service
    from postgresql_autocompletion_lib.helpers \
        import checkSyntax, getQueryText, getSettings
    from postgresql_autocompletion_lib.sqlparser import base_parse, \
        cursorPositionInQuery, parseFrom


class postgresql_autocompletion(sublime_plugin.EventListener):

    def __init__(self, db_talker=postgresql_query_service()):
        super(postgresql_autocompletion, self).__init__()
        self.db_query_service = db_talker
        pass

    def on_query_completions(self, view, prefix, locations):
        # Do nothing when it is not PostgreSQL script file
        self.settings = getSettings(view)
        if not checkSyntax(
                view,
                self.settings["postgresql_autocompletion_syntax"]):
            return []
        if not self.db_query_service.isConnected():
            self.dbConnect()
        query_text, cursor_pos = getQueryText(view)
        self.base_parse_results = base_parse(query_text)
        self.sql_block_at_cursor = cursorPositionInQuery(
            cursor_pos,
            self.base_parse_results)
        self.result = []
        if self.sql_block_at_cursor[0] == "from":
            self.process_from_clause()
        return self.result

    def process_from_clause(self):
        if self.sql_block_at_cursor[1] == '':
            self.addSchemasToResult(with_dot=True)
            self.addTablesToResult()
            return
        from_parse_results = parseFrom(self.sql_block_at_cursor[1])
        for from_element in from_parse_results:
            from_block = cursorPositionInQuery(
                self.sql_block_at_cursor[2],
                from_element)
            if from_block:
                if from_block[0] in ["schema_name"]:
                    self.addSchemasToResult()
                    return
                if from_block[0] == "schema_or_table_name":
                    self.addSchemasToResult(with_dot=True)
                    self.addTablesToResult()
                    return

    def addSchemasToResult(self, with_dot=False):
        schemas = self.db_query_service.getSchemas()
        if schemas:
            self.result += [
                [
                    schema_name + "\t" + "schema",
                    schema_name + ("." if with_dot else "")]
                for schema_name in schemas]

    def addTablesToResult(self):
        tables = self.db_query_service.getTables()
        if tables:
            self.result += [
                [table_name + "\t" + "table in " + schema_name,
                 table_name]
                for (table_name, schema_name) in tables]

    def dbConnect(self):
        self.db_query_service.connect(
            host=self.settings["postgresql_autocompletion_db_host"],
            port=self.settings["postgresql_autocompletion_db_port"],
            database=self.settings["postgresql_autocompletion_db_name"],
            user=self.settings["postgresql_autocompletion_db_user"],
            password=self.settings["postgresql_autocompletion_db_password"])
