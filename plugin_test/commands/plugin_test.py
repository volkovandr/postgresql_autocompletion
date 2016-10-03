import sublime
import sublime_plugin



class PluginTestCommand1(sublime_plugin.TextCommand):

    def run(self, edit):
        print("")
        print("View size is: ", self.view.size())
        s = self.view.settings().get("Zorro")
        print("View's setting Zorro is ", s)
        s2 = sublime.load_settings("plugin_test.sublime-settings").get("Zorro")
        print("Sublime's setting Zorro is ", s2)
        syntax = self.view.settings().get("syntax")
        print(syntax)
        print("Selection begin:", self.view.sel()[0].begin())

