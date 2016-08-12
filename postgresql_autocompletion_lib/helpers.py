'''Some functions that are used by the plugin'''


try:
    import sublime
    import sublime_plugin
except ImportError:
    import sublime_mocker
    import sublime_plugin_mocker
    sublime = sublime_mocker
    sublime_plugin = sublime_plugin_mocker


def checkSyntax(view):
    '''Checks if the file being edited is a PostgreSQL script'''
    if view.settings().get('syntax') == \
        ("Packages/PostgreSQL Syntax Highlighting" +
         "PostgreSQL.tmLanguage"):
        return True
    else:
        return False


def getQueryText(view):
    # searching backwards until semicolon
    beg = view.sel()[0].begin() - 1
    while view.substr(beg) != ";" and beg > 1:
        beg -= 1
    if view.substr(beg) == ";":
        beg += 2
    # searching forwards until the end of the file or until semicolon
    end = view.sel()[0].begin()
    while end < view.size():
        if view.substr(end) == ";":
            break
        end += 1
    query_text = \
        view.substr(view.word(sublime.Region(beg, end))).strip()
    return query_text
