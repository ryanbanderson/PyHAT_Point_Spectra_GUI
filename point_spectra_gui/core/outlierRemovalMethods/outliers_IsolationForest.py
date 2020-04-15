from PyQt5 import QtWidgets
from sklearn.ensemble import IsolationForest

from point_spectra_gui.ui.outliers_IsolationForest import Ui_Form
from point_spectra_gui.util.Modules import Modules


class Ui_Form(Ui_Form, IsolationForest, Modules):
    def setupUi(self, Form):
        super().setupUi(Form)
        self.checkMinAndMax()
        self.connectWidgets()

    def get_widget(self):
        return self.groupBox

    def setHidden(self, bool):
        self.get_widget().setHidden(bool)

    def connectWidgets(self):
        try:
            self.n_est_spin.setValue(self.n_estimators)
        except:
            pass
        try:
            self.prop_outliers_spin.setValue(self.contamination)
        except:
            pass

    def run(self):
        params = {
            'n_estimators': self.n_est_spin.value(),
            'contamination': self.prop_outliers_spin.value(),
            'n_jobs': -1}
        params_key = str(params)
        return params, params_key


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
