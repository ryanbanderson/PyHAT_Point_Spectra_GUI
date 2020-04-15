from PyQt5 import QtWidgets, QtCore
from sklearn.linear_model import ARDRegression

from point_spectra_gui.ui.cv_ARD import Ui_Form
from point_spectra_gui.util.Modules import Modules


class Ui_Form(Ui_Form, ARDRegression, Modules):
    def setupUi(self, Form):
        super().setupUi(Form)
        self.checkMinAndMax()
        self.connectWidgets()

    def get_widget(self):
        return self.formGroupBox

    def setHidden(self, bool):
        self.get_widget().setHidden(bool)

    def connectWidgets(self):
        self.numOfIterationsLineEdit.setText(str(self.n_iter))
        self.toleranceLineEdit.setText(str(self.tol))
        self.alpha1LineEdit.setText(str(self.alpha_1))
        self.alpha2LineEdit.setText(str(self.alpha_2))
        self.lambdaLineEdit.setText(str(self.lambda_1))
        self.lambdaLineEdit_2.setText(str(self.lambda_2))
        self.thresholdLambdaLineEdit.setText(str(self.threshold_lambda))
        self.fitIntercept_list.setCurrentItem(
            self.fitIntercept_list.findItems(str(self.fit_intercept), QtCore.Qt.MatchExactly)[0])
        self.normalize_list.setCurrentItem(
            self.normalize_list.findItems(str(self.normalize), QtCore.Qt.MatchExactly)[0])

    def run(self):
        fit_intercept_items = [i.text() == 'True' for i in self.fitIntercept_list.selectedItems()]
        normalize_items = [i.text() == 'True' for i in self.normalize_list.selectedItems()]

        params = {
            'n_iter': [int(i) for i in self.numOfIterationsLineEdit.text().split(',')],
            'tol': [float(i) for i in self.toleranceLineEdit.text().split(',')],
            'alpha_1': [float(i) for i in self.alpha1LineEdit.text().split(',')],
            'alpha_2': [float(i) for i in self.alpha2LineEdit.text().split(',')],
            'lambda_1': [float(i) for i in self.lambdaLineEdit.text().split(',')],
            'lambda_2': [float(i) for i in self.lambdaLineEdit_2.text().split(',')],
            'compute_score': [False],
            'threshold_lambda': [float(i) for i in self.thresholdLambdaLineEdit.text().split(',')],
            'fit_intercept': fit_intercept_items,
            'normalize': normalize_items,
            'copy_X': [True],
            'verbose': [True]}

        return params


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
