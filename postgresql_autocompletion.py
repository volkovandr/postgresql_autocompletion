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
    import checkSyntax, getQueryText
from postgresql_autocompletion_lib.sqlparser import base_parse, \
    cursorPositionInQuery, parseFrom, cursorPositionInFrom


class postgresql_autocompletion(sublime_plugin.EventListener):

    def __init__(self, db_talker=postgresql_query_service()):
        super(postgresql_autocompletion, self).__init__()
        self.db_query_service = db_talker
        pass

    def on_query_completions(self, view, prefix, locations):
        # Do nothing when it is not PostgreSQL script file
        if not checkSyntax(view):
            return []
        query_text, cursor_pos = getQueryText(view)
        base_parse_results = base_parse(query_text)
        sql_block = cursorPositionInQuery(cursor_pos, base_parse_results)
        if sql_block[0] == "from":
            from_parse_results = parseFrom(sql_block[1])
            from_block = cursorPositionInFrom(sql_block[2], from_parse_results)
            if from_block[0] == "schema_name":
                schemas = db_query_service.getSchemas()
                return schemas
