import numpy as np
from PyQt5 import QtWidgets, QtCore

from point_spectra_gui.ui.caltran_PDS import Ui_Form
from point_spectra_gui.util.Modules import Modules


class Ui_Form(Ui_Form, Modules):
    def setupUi(self, Form):
        super().setupUi(Form)
        self.connectWidgets()

    def get_widget(self):
        return self.formGroupBox

    def setHidden(self, bool):
        self.get_widget().setHidden(bool)

    def connectWidgets(self):
        self.toggle_pls()
        self.pls_checkbox.stateChanged.connect(self.toggle_pls)
        self.winsize_spin.valueChanged.connect(lambda: self.pls_spin.setMaximum(self.winsize_spin.value()-1))

    def toggle_pls(self):
        if self.pls_checkbox.isChecked():
            self.pls_nc_label.setHidden(False)
            self.pls_spin.setHidden(False)
        else:
            self.pls_nc_label.setHidden(True)
            self.pls_spin.setHidden(True)


    def run(self):
        window_size = self.winsize_spin.value()
        use_pls = self.pls_checkbox.isChecked()
        pls_nc = self.pls_spin.value()
        params = {'win_size': window_size,
                  'pls': use_pls,
                  'nc': pls_nc}

        return params


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
