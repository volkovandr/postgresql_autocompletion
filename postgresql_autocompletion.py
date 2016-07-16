'''This is the main module for Sublime plugin PostgeSQL autocompletion'''

try:
    import sublime
    import sublime_plugin
except ImportError:
    import sublime_mocker
    import sublime_plugin_mocker
    sublime = sublime_mocker
    sublime_plugin = sublime_plugin_mocker


print(sublime)
print(sublime_plugin)

print("test")
