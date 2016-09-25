'''This is the main module for Sublime plugin PostgeSQL autocompletion'''

try:
    import sublime
    import sublime_plugin
except ImportError:
    import sublime_mocker
    import sublime_plugin_mocker
    sublime = sublime_mocker
    sublime_plugin = sublime_plugin_mocker

from postgresql_autocompletion_lib.postgresql_query_service \
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
        if not checkSyntax(view, self.settings["postgresql_autocompletion_syntax"]):
            return []
        query_text, cursor_pos = getQueryText(view)
        self.base_parse_results = base_parse(query_text)
        self.sql_block_at_cursor = cursorPositionInQuery(
            cursor_pos,
            self.base_parse_results)
        if self.sql_block_at_cursor[0] == "from":
            return self.process_from_clause()

    def process_from_clause(self):
        from_parse_results = parseFrom(self.sql_block_at_cursor[1])
        for from_element in from_parse_results:
            from_block = cursorPositionInQuery(
                self.sql_block_at_cursor[2],
                from_element)
            if from_block:
                if from_block[0] == "schema_name":
                    schemas = self.db_query_service.getSchemas()
                    return schemas

