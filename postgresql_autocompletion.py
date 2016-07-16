'''This is the main module for Sublime plugin PostgeSQL autocompletion'''

try:
    import sublime
    import sublime_plugin
except ImportError:
    import sublime_mocker
    import sublime_plugin_mocker
    sublime = sublime_mocker
    sublime_plugin = sublime_plugin_mocker


class postgresql_autocompletion(sublime_plugin.EventListener):

    def on_query_completions(self, view, prefix, locations):
        pass
