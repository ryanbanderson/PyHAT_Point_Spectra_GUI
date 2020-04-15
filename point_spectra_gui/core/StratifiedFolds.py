from PyQt5 import QtWidgets

from point_spectra_gui.ui.StratifiedFolds import Ui_Form
from point_spectra_gui.util.Modules import Modules
from point_spectra_gui.util.spectral_data import spectral_data
from libpyhat.utils.folds import stratified_folds
from libpyhat.utils.utils import rows_match
import copy
from point_spectra_gui.core.Plot import Plot
# from point_spectra_gui.util import plots
import numpy as np
import matplotlib.pyplot as plt

class StratifiedFolds(Ui_Form, Modules):

    def setupUi(self, Form):
        super().setupUi(Form)
        Modules.setupUi(self, Form)

    def get_widget(self):
        return self.formGroupBox

    def connectWidgets(self):
        self.setComboBox(self.chooseDataToStratifyComboBox, self.datakeys)
        try:  # Some instances where perhaps there is no data to load
            data = self.data[self.chooseDataToStratifyComboBox.currentText()].df['comp'].columns.values
            self.setComboBox(self.chooseVarComboBox, data)
        except:
            pass
        self.chooseDataToStratifyComboBox.activated[int].connect(self.strat_fold_change_vars)
        self.nFoldsSpinBox.valueChanged.connect(self.strat_fold_change_testfolds)

    def run(self):
        Modules.data_count += 1
        self.train_ind = Modules.data_count
        Modules.data_count += 1
        self.test_ind = Modules.data_count

        datakey = self.chooseDataToStratifyComboBox.currentText()
        nfolds = self.nFoldsSpinBox.value()
        try:
            testfold = int(self.testFoldsSpinBox.value())
        except:
            testfold = 1
        colname = ('comp', self.chooseVarComboBox.currentText())
        self.data[datakey]=spectral_data(stratified_folds(self.data[datakey].df,nfolds=nfolds, sortby=colname))
        self.data[datakey + '-Train'] = spectral_data(rows_match(self.data[datakey].df,('meta', 'Folds'), [testfold], invert=True))
        self.data[datakey + '-Test'] = spectral_data(rows_match(self.data[datakey].df,('meta', 'Folds'), [testfold]))
        self.list_amend(self.datakeys,self.train_ind,datakey + '-Train')
        self.list_amend(self.datakeys, self.test_ind, datakey + '-Test')
        print(self.datakeys)
        print('Test set: '+str(self.data[datakey + '-Test'].df.index.shape[0]))
        print('Training set: '+str(self.data[datakey + '-Train'].df.index.shape[0]))


    def strat_fold_change_vars(self):
        self.chooseVarComboBox.clear()
        try:
            choices = self.data[self.chooseDataToStratifyComboBox.currentText()].df['comp'].columns.values
        except:
            choices = ['No composition columns!']

        self.chooseVarComboBox.addItems(choices)

    def strat_fold_change_testfolds(self):
        self.testFoldsSpinBox.setMaximum(self.nFoldsSpinBox.value())


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    Form = QtWidgets.QWidget()
    ui = StratifiedFolds()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
