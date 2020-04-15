from PyQt5 import QtWidgets
from libpyhat.transform.baseline_code.als import ALS

from point_spectra_gui.ui.ALS import Ui_Form
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
        als = ALS()

        self.asymmetryDoubleSpinBox.setDecimals(2)
        self.smoothnessDoubleSpinBox.setMaximum(10000000)
        self.convergenceThresholdDoubleSpinBox.setDecimals(6)

        self.asymmetryDoubleSpinBox.setValue(als.asymmetry_param)
        self.smoothnessDoubleSpinBox.setValue(als.smoothness_param)
        self.maxNumOfIterationsSpinBox.setValue(als.max_iters)
        self.convergenceThresholdDoubleSpinBox.setValue(als.conv_thresh)

    def run(self):
        methodParameters = {'asymmetry_param': self.asymmetryDoubleSpinBox.value(),
                            'smoothness_param': self.smoothnessDoubleSpinBox.value(),
                            'max_iters': self.maxNumOfIterationsSpinBox.value(),
                            'conv_thresh': self.convergenceThresholdDoubleSpinBox.value()}
        return methodParameters, self.getChangedValues(methodParameters, ALS())


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
