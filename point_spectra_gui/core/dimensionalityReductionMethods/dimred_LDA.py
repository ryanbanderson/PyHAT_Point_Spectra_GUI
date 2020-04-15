from PyQt5 import QtWidgets
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from point_spectra_gui.ui.dimred_LDA import Ui_Form
from point_spectra_gui.util.Modules import Modules


class Ui_Form(Ui_Form, LinearDiscriminantAnalysis, Modules):
    def setupUi(self, Form):
        super().setupUi(Form)
        self.checkMinAndMax()
        self.connectWidgets()

    def get_widget(self):
        return self.groupBox

    def setHidden(self, bool):
        self.get_widget().setHidden(bool)

    def connectWidgets(self):
        self.nc_spin.setValue(8)

    def update(self,new_y_choices):
        self.changeComboListVars(self.class_combo, new_y_choices)

    def run(self):

        params = {
            'n_components': self.nc_spin.value()}
        params_key = str(params)
        ycol = self.class_combo.currentText()
        return params, params_key, ycol



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())