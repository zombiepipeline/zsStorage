from . import python

reload(python)

class appRename:
    module = None

    def init_app(self):
        python.app.show_dialog(self)

    def show_dialog(self, module):
        self.module = module

app_rename = appRename()
app_rename.init_app()