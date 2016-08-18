'''This is the main module for Sublime plugin PostgeSQL autocompletion'''

try:
    import sublime
    import sublime_plugin
except ImportError:
    from .mockers import sublime_mocker
    from .mockers import sublime_plugin_mocker
    sublime = sublime_mocker
    sublime_plugin = sublime_plugin_mocker

from postgresql_autocompletion_lib.helpers import *


class postgresql_autocompletion(sublime_plugin.EventListener):

    def on_query_completions(self, view, prefix, locations):
        # Do nothing when it is not PostgreSQL script file
        if not checkSyntax(view):
            return []

