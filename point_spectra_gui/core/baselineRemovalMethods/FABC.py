from PyQt5 import QtWidgets
from libpyhat.transform.baseline_code.fabc import FABC

from point_spectra_gui.ui.FABC import Ui_Form
from point_spectra_gui.util.Modules import Modules


class Ui_Form(Ui_Form, Modules):
    def setupUi(self, Form):
        super().setupUi(Form)
        self.checkMinAndMax()
        Modules.setupUi(self, Form)

    def get_widget(self):
        return self.groupBox

    def setHidden(self, bool):
        self.get_widget().setHidden(bool)

    def connectWidgets(self):
        br = FABC()
        self.smoothnessDoubleSpinBox.setValue(br.dilation_param)
        self.dilationSpinBox.setValue(br.smoothness_param)

    def run(self):
        methodParameters = {'dilation_param': self.smoothnessDoubleSpinBox.value(),
                            'smoothness_param': self.dilationSpinBox.value()}
        return methodParameters, self.getChangedValues(methodParameters, FABC())


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
