from PyQt5 import QtWidgets
from libpyhat.transform.baseline_code.polyfit import PolyFit

from point_spectra_gui.ui.Polyfit import Ui_Form
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
        br = PolyFit()
        self.orderSpinBox.setValue(br.poly_order)
        self.numOfStandardDeviationsSpinBox.setValue(br.num_stdv)

    def run(self):
        methodParameters = {'poly_order': self.orderSpinBox.value(),
                            'num_stdv': self.numOfStandardDeviationsSpinBox.value()}
        return methodParameters, self.getChangedValues(methodParameters, PolyFit())


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
