'''Some functions that are used by the plugin'''


try:
    import sublime
    import sublime_plugin
except ImportError:
    import sublime_mocker
    import sublime_plugin_mocker
    sublime = sublime_mocker
    sublime_plugin = sublime_plugin_mocker


def checkSyntax(view, syntax):
    '''Checks if the file being edited is a PostgreSQL script'''
    return syntax in view.settings().get('syntax')


def getQueryText(view):
    '''Returns the text of the current query (at the cursor)
    and the position of the cursor relative to the beginning of the query'''
    # searching backwards until semicolon
    print(view.size())
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
    cursor_pos = view.sel()[0].begin() - \
        view.word(sublime.Region(beg, end)).begin() - \
        (len(query_text) - len(query_text.lstrip()))
    if cursor_pos > len(query_text):
        cursor_pos = len(query_text)
    return (query_text, cursor_pos)


def getSetting(view, setting_name):
    '''Looks for the given setting in the projects settings when not found then
    in the global settings'''
    view_setting = view.settings().get(setting_name)
    if view_setting is not None:
        return view_setting
    global_setting = sublime.load_settings(
        "postgresql_autocompletion.sublime-settings").get(setting_name)
    return global_setting


def getSettings(view):
    '''Returns all the settings as dictionary.
    The missing settings will get their default values.
    The new settings that could be found in the settings file are ignored'''
    settings = {
        "postgresql_autocompletion_db_host": "localhost",
        "postgresql_autocompletion_db_port": "5432",
        "postgresql_autocompletion_db_name": "postgres",
        "postgresql_autocompletion_db_user": "user",
        "postgresql_autocompletion_db_password": "password",
        "postgresql_autocompletion_syntax": "PostgreSQL"}
    for setting_key in settings:
        setting_value = getSetting(view, setting_key)
        if setting_value is not None:
            settings[setting_key] = setting_value
    return settings
