import numpy as np
from PyQt5 import QtWidgets, QtCore

from point_spectra_gui.ui.caltran_DS import Ui_Form
from point_spectra_gui.util.Modules import Modules

class Ui_Form(Ui_Form, Modules):
    def setupUi(self, Form):
        super().setupUi(Form)
     #   self.connectWidgets()

    def get_widget(self):
        return self.groupBox

    def setHidden(self, bool):
        self.get_widget().setHidden(bool)

    def run(self):
        self.fit_intercept = self.fit_intercept_checkBox.isChecked()
        params = {'fit_intercept': self.fit_intercept
                  }

        return params


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
