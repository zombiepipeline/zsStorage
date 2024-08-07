from . import python

reload(python)

class appBlast:
    module = None

    def init_app(self):
        python.app.show_dialog(self)

    def show_dialog(self, module):
        self.module = module

initializate = appBlast()
initializate.init_app()