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
from postgresql_autocompletion_lib.helpers import checkSyntax


class postgresql_autocompletion(sublime_plugin.EventListener):

    def __init__(self, db_talker=postgresql_query_service()):
        super(postgresql_autocompletion, self).__init__()
        self.db_query_service = db_talker
        pass

    def on_query_completions(self, view, prefix, locations):
        # Do nothing when it is not PostgreSQL script file
        if not checkSyntax(view):
            return []
        # get query text and cursor position
        # parse the query and determine in which part of the query is the cursor
        # depending on the active part of the query suggest different autocompletion options
