from PyQt5 import QtWidgets, QtCore
from sklearn.linear_model.base import LinearRegression

from point_spectra_gui.ui.cv_OLS import Ui_Form
from point_spectra_gui.util.Modules import Modules


class Ui_Form(Ui_Form, LinearRegression, Modules):
    def setupUi(self, Form):
        super().setupUi(Form)
        self.checkMinAndMax()
        self.connectWidgets()

    def get_widget(self):
        return self.groupBox

    def setHidden(self, bool):
        self.get_widget().setHidden(bool)

    def connectWidgets(self):
        self.fit_intercept_list.setCurrentItem(
            self.fit_intercept_list.findItems(str(self.fit_intercept), QtCore.Qt.MatchExactly)[0])

    def run(self):
        fit_intercept_items = [i.text() == 'True' for i in self.fit_intercept_list.selectedItems()]
        params = {'fit_intercept': fit_intercept_items}

        return params


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
