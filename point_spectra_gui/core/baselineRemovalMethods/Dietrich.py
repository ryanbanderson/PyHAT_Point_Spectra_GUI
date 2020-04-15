from PyQt5 import QtWidgets
from libpyhat.transform.baseline_code.dietrich import Dietrich

from point_spectra_gui.ui.Dietrich import Ui_Form
from point_spectra_gui.util.Modules import Modules

class Ui_Form(Ui_Form, Modules):
    def setupUi(self, Form):
        super().setupUi(Form)
        Modules.setupUi(self, Form)

    def get_widget(self):
        return self.groupbox

    def setHidden(self, bool):
        self.get_widget().setHidden(bool)

    def connectWidgets(self):
        br = Dietrich()
        self.halfWindowSpinBox.setValue(br.half_window)
        self.numOfErosionsSpinBox.setValue(br.num_erosions)

    def run(self):
        methodParameters = {'half_window': self.halfWindowSpinBox.value(),
                            'num_erosions': self.numOfErosionsSpinBox.value()}
        return methodParameters, self.getChangedValues(methodParameters, Dietrich())


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
