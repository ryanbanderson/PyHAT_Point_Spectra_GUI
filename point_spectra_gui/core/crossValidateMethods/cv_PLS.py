from PyQt5 import QtWidgets
from sklearn.cross_decomposition.pls_ import PLSRegression

from point_spectra_gui.ui.cv_PLS import Ui_Form
from point_spectra_gui.util.Modules import Modules


class Ui_Form(Ui_Form, PLSRegression, Modules):
    def setupUi(self, Form):
        super().setupUi(Form)
        self.checkMinAndMax()
        self.connectWidgets()

    def get_widget(self):
        return self.formGroupBox

    def setHidden(self, bool):
        self.get_widget().setHidden(bool)

    def connectWidgets(self):
        self.numOfComponentsLineEdit.setText('1,2,3,4,5,6,7,8,9,10,11,12,13,14,15')

    def run(self):
        params = {'n_components': [int(i) for i in self.numOfComponentsLineEdit.text().split(',')],
                  'scale': [False]}
        return params


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
