from PyQt5 import QtWidgets

from point_spectra_gui.ui.CalibrationTransfer import Ui_Form
from point_spectra_gui.util.Modules import Modules
from point_spectra_gui.core.caltranMethods import *
from libpyhat.transform import cal_tran
from libpyhat.transform import caltran_utils
import pandas as pd
import numpy as np

class CalibrationTransfer(Ui_Form, Modules):

    def setupUi(self, Form):
        super().setupUi(Form)
        Modules.setupUi(self, Form)
        self.caltranMethods()

    def get_widget(self):
        return self.formGroupBox

    def connectWidgets(self):
        self.methodlist = ['PDS - Piecewise DS',
         'DS - Direct Standardization',
         'LASSO DS',
         'Ridge DS',
         'CCA - Canonical Correlation Analysis',
         'New CCA',
         'Incremental Proximal Descent DS',
         'Forward Backward DS',
         'Sparse Low Rank DS',
         'PDS-PLS - PDS using Partial Least Squares']

        self.setComboBox(self.chooseDataA, self.datakeys)
        self.setComboBox(self.chooseDataB, self.datakeys)
        self.setComboBox(self.chooseDatatoTransform,self.datakeys)
        try:
            self.setComboBox(self.chooseDataAMatch, self.data[self.chooseDataA.currentText()].df['meta'].columns.values)
            self.setComboBox(self.chooseDataBMatch, self.data[self.chooseDataB.currentText()].df['meta'].columns.values)
        except:
            pass

        self.chooseDataA.activated.connect(lambda: self.change_choices(self.chooseDataAMatch,self.chooseDataA))
        self.chooseDataB.activated.connect(lambda: self.change_choices(self.chooseDataBMatch, self.chooseDataB))
        self.chooseMethod.currentIndexChanged.connect(
            lambda: self.make_caltran_widget(self.chooseMethod.currentText()))

    def make_caltran_widget(self, alg, params=None):
        self.hideAll()
        print(alg)
        try:
            self.alg[alg].setHidden(False)
        except:
            pass

    def hideAll(self):
        for a in self.alg:
            self.alg[a].setHidden(True)

    def caltranMethods(self):
        self.alg = {'PDS - Piecewise DS': caltran_PDS.Ui_Form(),
                    'DS - Direct Standardization': caltran_DS.Ui_Form(),
                    'LASSO DS': caltran_LASSODS.Ui_Form(),
                    'Ridge DS': caltran_RidgeDS.Ui_Form(),
                    'CCA - Canonical Correlation Analysis': caltran_CCA.Ui_Form(),
                    'New CCA': caltran_NewCCA.Ui_Form(),
                    'Incremental Proximal Descent DS': caltran_IPDDS.Ui_Form(),
                    'Forward Backward DS': caltran_FBDS.Ui_Form(),
                    'Sparse Low Rank DS': caltran_SparseDS.Ui_Form(),
                    'Ratio': caltran_Ratio.Ui_Form(),
                    'PDS-PLS - PDS using Partial Least Squares': caltran_cv_PDS_PLS.Ui_Form()
                    }

        for item in self.alg:
            self.alg[item].setupUi(self.Form)
            self.methodlayout.addWidget(self.alg[item].get_widget())
            self.alg[item].setHidden(True)

    def change_choices(self, combobox, datacombo):
        combobox.clear()
        try:
            choices = self.data[datacombo.currentText()].df['meta'].columns.values
        except:
            choices = ['No metadata columns!']

        combobox.addItems(choices)

    def run(self):
        datakeyA = self.chooseDataA.currentText()
        datakeyB = self.chooseDataB.currentText()
        datakeyC = self.chooseDatatoTransform.currentText()
        dataAmatchcol = self.chooseDataAMatch.currentText()
        dataBmatchcol = self.chooseDataBMatch.currentText()

        #get the data sets
        A = self.data[datakeyA].df
        B = self.data[datakeyB].df
        C = self.data[datakeyC].df

        assert (len(B['wvl'].columns) == len(C['wvl'].columns)),\
            'Data sets B and C have different numbers of spectral channels!'
        assert (B['wvl'].columns.values[-1] == C['wvl'].columns.values[-1]),\
            "Data set B and C wavelengths are not identical. Check rounding and/or resample one data set onto the other's wavelengths"
        A_mean, B_mean = caltran_utils.prepare_data(A, B, dataAmatchcol, dataBmatchcol)

        method = self.chooseMethod.currentText()
        params = self.alg[method].run()
        params['method']=method
        ct_obj = cal_tran.cal_tran(params)
        print('Deriving transform from '+datakeyA+' to '+datakeyB+' using '+method)
        ct_obj.derive_transform(A_mean['wvl'],B_mean['wvl'])

        print('Applying transform to '+datakeyC)
        C_transform = ct_obj.apply_transform(C['wvl'])
        self.data[datakeyC].df['wvl'] = C_transform



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    Form = QtWidgets.QWidget()
    ui = CalibrationTransfer()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
