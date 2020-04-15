import numpy as np
from PyQt5 import QtWidgets, QtCore

from point_spectra_gui.ui.caltran_cv_DS import Ui_Form
from point_spectra_gui.util.Modules import Modules

class Ui_Form(Ui_Form, Modules):
    def setupUi(self, Form):
        super().setupUi(Form)
     #   self.connectWidgets()

    def get_widget(self):
        return self.groupBox

    def setHidden(self, bool):
        self.get_widget().setHidden(bool)

    # def connectWidgets(self):
    #     self.fit_intercept_list.setCurrentItem(
    #         self.fit_intercept_list.findItems(str(self.fit_intercept), QtCore.Qt.MatchExactly)[0])

    def run(self):
        self.fit_intercept = [i.text() == 'True' for i in self.fit_intercept_list.selectedItems()]
        params = {'method':['DS - Direct Standardization'],
                  'fit_intercept': self.fit_intercept
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
