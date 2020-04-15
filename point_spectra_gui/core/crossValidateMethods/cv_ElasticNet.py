import numpy as np
from PyQt5 import QtWidgets, QtCore
from sklearn.linear_model import ElasticNet

from point_spectra_gui.ui.cv_ElasticNet import Ui_Form
from point_spectra_gui.util.Modules import Modules


class Ui_Form(Ui_Form, ElasticNet, Modules):
    def setupUi(self, Form):
        super().setupUi(Form)
        self.checkMinAndMax()
        self.connectWidgets()

    def get_widget(self):
        return self.elasticNetGroupBox

    def setHidden(self, bool):
        self.get_widget().setHidden(bool)

    def connectWidgets(self):
        en = ElasticNet()
        self.minalpha_spin.setDecimals(20)
        self.maxalpha_spin.setDecimals(20)

        self.minalpha_spin.setValue(0.000000000000001)
        self.maxalpha_spin.setValue(0.01)
        self.nalpha_spin.setValue(100)

        self.enl1_ratioLineEdit.setText('0.1, 0.5, 0.7, 0.9, 0.95, 0.99, 1.0')
        self.enfit_intercept_list.setCurrentItem(
            self.enfit_intercept_list.findItems(str(en.fit_intercept), QtCore.Qt.MatchExactly)[0])
        self.enmax_iterLineEdit.setText(str(en.max_iter))
        self.entolLineEdit.setText(str(en.tol))
        self.enpositive_list.setCurrentItem(self.enpositive_list.findItems(str(en.positive), QtCore.Qt.MatchExactly)[0])

    def run(self):
        fit_intercept_items = [i.text() == 'True' for i in self.enfit_intercept_list.selectedItems()]
        positive_items = [i.text() == 'True' for i in self.enpositive_list.selectedItems()]
        alphas = np.logspace(np.log10(self.minalpha_spin.value()), np.log10(self.maxalpha_spin.value()),
                             num=self.nalpha_spin.value())
        params = {
            'l1_ratio': [float(i) for i in self.enl1_ratioLineEdit.text().split(',')],
            'fit_intercept': fit_intercept_items,
            'max_iter': [int(i) for i in self.enmax_iterLineEdit.text().split(',')],
            'tol': [float(i) for i in self.entolLineEdit.text().split(',')],
            'precompute': [True],
            'copy_X': [True],
            'positive': positive_items,
            'selection': ['random']}

        return params, list(alphas)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
