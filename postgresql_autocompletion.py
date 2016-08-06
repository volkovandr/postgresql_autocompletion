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
        # Do nothing when it is not PostgreSQL script file
        if not self.checkSyntax(view):
            return []
        query = getQueryText(view)

    def checkSyntax(self, view):
        if view.settings().get('syntax') == \
                "Packages/PostgreSQL Syntax Highlighting/\
PostgreSQL.tmLanguage":
            return True
        else:
            return False

    def getQueryText(self, view):
        # searching backwards until semicolon
        beg = view.sel()[0].begin() - 1
        while view.substr(beg) != ";" and beg > 0:
            beg = beg - 1
        if view.substr(beg) == ";":
            beg = beg + 2
        # searching forwards until the end of the file or until semicolon
        end = view.sel()[0].begin()
        while view.substr(end) != ";" and end < view.size():
            end = end + 1
        query_text = \
            view.substr(view.word(sublime.Region(beg, end))).strip() + "\n"
        return query_text
