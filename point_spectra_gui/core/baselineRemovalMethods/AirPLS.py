from PyQt5 import QtWidgets
from libpyhat.transform.baseline_code.airpls import AirPLS

from point_spectra_gui.ui.AirPLS import Ui_Form
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
        airPLS = AirPLS()
        self.smoothnessSpinBox.setValue(airPLS.smoothness_param)
        self.convergenceThresholdDoubleSpinBox.setValue(airPLS.conv_thresh)
        self.maxNumOfIterationsSpinBox.setValue(airPLS.max_iters)

    def run(self):
        methodParameters = {'smoothness_param': float(self.smoothnessSpinBox.value()),
                            'conv_thresh': float(self.convergenceThresholdDoubleSpinBox.value()),
                            'max_iters': float(self.maxNumOfIterationsSpinBox.value())}

        return methodParameters, self.getChangedValues(methodParameters, AirPLS())


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
