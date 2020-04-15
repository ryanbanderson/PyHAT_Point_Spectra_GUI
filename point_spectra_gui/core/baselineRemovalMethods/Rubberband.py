from PyQt5 import QtWidgets
from libpyhat.transform.baseline_code.rubberband import Rubberband

from point_spectra_gui.ui.Rubberband import Ui_Form
from point_spectra_gui.util.Modules import Modules


class Ui_Form(Ui_Form, Modules):
    def setupUi(self, Form):
        super().setupUi(Form)
        self.checkMinAndMax()
        Modules.setupUi(self, Form)

    def get_widget(self):
        return self.groupbox

    def setHidden(self, bool):
        self.get_widget().setHidden(bool)

    def connectWidgets(self):
        br = Rubberband()
        self.n_iter_spin.setValue(br.num_iters)
        self.numOfRangesSpinBox.setValue(br.num_ranges)

    def run(self):

        methodParameters = {'num_iters': self.n_iter_spin.value(),
                            'num_ranges': self.numOfRangesSpinBox.value()}
        return methodParameters, self.getChangedValues(methodParameters, Rubberband())


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
