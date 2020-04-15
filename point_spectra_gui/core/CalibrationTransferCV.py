from PyQt5 import QtWidgets
from point_spectra_gui.util import Qtickle
from point_spectra_gui.ui.CalibrationTransferCV import Ui_Form
from point_spectra_gui.util.Modules import Modules
from point_spectra_gui.core.caltranMethods import *
from point_spectra_gui.util import spectral_data
from libpyhat.transform import cal_tran, caltran_utils
import pandas as pd
import numpy as np
from sklearn.model_selection import ParameterGrid, LeaveOneGroupOut
import copy

def mismatch_rmse(spectrum, spectrum_to_match):
    return np.sqrt(np.mean((spectrum - spectrum_to_match)**2))


class CalibrationTransferCV(Ui_Form, Modules):

    def setupUi(self, Form):
        super().setupUi(Form)
        Modules.setupUi(self, Form)
        self.caltranMethods()

    def get_widget(self):
        return self.formGroupBox

    def connectWidgets(self):

        self.setComboBox(self.chooseDataA, self.datakeys)
        self.setComboBox(self.chooseDataB, self.datakeys)
        try:
            self.setComboBox(self.chooseDataAMatch, self.data[self.chooseDataA.currentText()].df['meta'].columns.values)
            self.setComboBox(self.chooseDataBMatch, self.data[self.chooseDataB.currentText()].df['meta'].columns.values)
        except:
            pass

        self.chooseDataA.activated.connect(lambda: self.change_choices(self.chooseDataAMatch,self.chooseDataA))
        self.chooseDataB.activated.connect(lambda: self.change_choices(self.chooseDataBMatch, self.chooseDataB))
        self.DScheckbox.stateChanged.connect(
            lambda: self.toggle_caltran_widget('DS - Direct Standardization',self.DScheckbox.isChecked()))
        self.PDScheckbox.stateChanged.connect(
            lambda: self.toggle_caltran_widget('PDS - Piecewise DS',self.PDScheckbox.isChecked()))
        self.LASSODScheckbox.stateChanged.connect(
            lambda: self.toggle_caltran_widget('LASSO DS',self.LASSODScheckbox.isChecked()))
        self.PDSPLScheckBox.stateChanged.connect(
            lambda: self.toggle_caltran_widget('PDS-PLS - PDS using Partial Least Squares',self.PDSPLScheckBox.isChecked()))
        self.RidgeDScheckBox.stateChanged.connect(
            lambda: self.toggle_caltran_widget('Ridge DS',self.RidgeDScheckBox.isChecked()))
        self.CCAcheckBox.stateChanged.connect(
            lambda: self.toggle_caltran_widget('CCA - Canonical Correlation Analysis',self.CCAcheckBox.isChecked()))
        self.IPDDScheckBox.stateChanged.connect(
            lambda: self.toggle_caltran_widget('Incremental Proximal Descent DS',self.IPDDScheckBox.isChecked()))
        self.NewCCAcheckBox.stateChanged.connect(
            lambda: self.toggle_caltran_widget('New CCA',self.NewCCAcheckBox.isChecked()))
        self.ForwardBackwardcheckBox.stateChanged.connect(
            lambda: self.toggle_caltran_widget('Forward Backward DS',self.ForwardBackwardcheckBox.isChecked()))
        self.SparseDScheckBox.stateChanged.connect(
            lambda: self.toggle_caltran_widget('Sparse Low Rank DS', self.SparseDScheckBox.isChecked()))

    def getGuiParams(self):
        """
        Overriding Modules' getGuiParams, because I'll need to do a list of lists
        in order to obtain the regressionMethods' parameters
        """
        self.qt = Qtickle.Qtickle(self)
        s = []
        s.append(self.qt.guiSave())
        for items in self.alg:
            s.append(self.alg[items][0].getGuiParams())
        return s

    def setGuiParams(self, dict):
        self.qt = Qtickle.Qtickle(self)
        self.qt.guiRestore(dict[0])
        keys = list(self.alg.keys())
        for i in range(len(dict)):
            self.alg[keys[i - 1]][0].setGuiParams(dict[i])

    def selectiveSetGuiParams(self, dict):
        """
        Override Modules' selective Restore function

        Setup Qtickle
        selectively restore the UI, the data to do that will be in the 0th element of the dictionary
        We will then iterate through the rest of the dictionary
        Will now restore the parameters for the algorithms in the list, Each of the algs have their own selectiveSetGuiParams

        :param dict:
        :return:
        """
        self.qt = Qtickle.Qtickle(self)
        self.qt.selectiveGuiRestore(dict[0])
        keys = list(self.alg.keys())
        for i in range(len(dict)):
            self.alg[keys[i - 1]][0].selectiveSetGuiParams(dict[i])

    def toggle_caltran_widget(self, alg, state):
        if state:
            self.alg[alg][0].setHidden(False)
        else:
            self.alg[alg][0].setHidden(True)

    def hideAll(self):
        for a in self.alg:
            self.alg[a][0].setHidden(True)

    def caltranMethods(self):
        self.alg = {'PDS - Piecewise DS': [caltran_cv_PDS.Ui_Form(), self.PDSlayout],
                    'PDS-PLS - PDS using Partial Least Squares': [caltran_cv_PDS_PLS.Ui_Form(), self.PDSPLSlayout],
                    'DS - Direct Standardization': [caltran_cv_DS.Ui_Form(),self.DSlayout],
                    'LASSO DS': [caltran_cv_LASSODS.Ui_Form(), self.LASSODSlayout],
                    'Ridge DS': [caltran_cv_RidgeDS.Ui_Form(), self.RidgeDSlayout],
                    'CCA - Canonical Correlation Analysis': [caltran_cv_CCA.Ui_Form(),self.CCAlayout],
                    'New CCA': [caltran_cv_NewCCA.Ui_Form(),self.NewCCALayout],
                    'Incremental Proximal Descent DS': [caltran_cv_IPDDS.Ui_Form(), self.IPDDSlayout],
                    'Forward Backward DS': [caltran_cv_FBDS.Ui_Form(), self.FBDSlayout],
                    'Sparse Low Rank DS': [caltran_cv_SparseDS.Ui_Form(),self.SparseLayout]}

        for key in self.alg.keys():
            self.alg[key][0].setupUi(self.Form)
            self.alg[key][1].addWidget(self.alg[key][0].get_widget())
            self.alg[key][0].setHidden(True)


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
        dataAmatchcol = self.chooseDataAMatch.currentText()
        dataBmatchcol = self.chooseDataBMatch.currentText()

        paramgrid = [{'method':'None'}]
        if self.PDScheckbox.isChecked():
            paramgrid.extend(list(ParameterGrid(self.alg['PDS - Piecewise DS'][0].run())))
        if self.PDSPLScheckBox.isChecked():
            paramgrid.extend(list(ParameterGrid(self.alg['PDS-PLS - PDS using Partial Least Squares'][0].run())))
        if self.DScheckbox.isChecked():
            paramgrid.extend(list(ParameterGrid(self.alg['DS - Direct Standardization'][0].run())))
        if self.LASSODScheckbox.isChecked():
            paramgrid.extend(list(ParameterGrid(self.alg['LASSO DS'][0].run())))
        if self.Ratiocheckbox.isChecked():
            paramgrid.extend([{'method':'Ratio'}])
        if self.SparseDScheckBox.isChecked():
            paramgrid.extend(list(ParameterGrid(self.alg['Sparse Low Rank DS'][0].run())))
        if self.RidgeDScheckBox.isChecked():
            paramgrid.extend(list(ParameterGrid(self.alg['Ridge DS'][0].run())))
        if self.CCAcheckBox.isChecked():
            paramgrid.extend(list(ParameterGrid(self.alg['CCA - Canonical Correlation Analysis'][0].run())))
        if self.NewCCAcheckBox.isChecked():
            paramgrid.extend(list(ParameterGrid(self.alg['New CCA'][0].run())))
        if self.ForwardBackwardcheckBox.isChecked():
            paramgrid.extend(list(ParameterGrid(self.alg['Forward Backward DS'][0].run())))
        if self.IPDDScheckBox.isChecked():
            paramgrid.extend(list(ParameterGrid(self.alg['Incremental Proximal Descent DS'][0].run())))

        #get the data sets
        A = self.data[datakeyA].df
        B = self.data[datakeyB].df
        A_mean,B_mean = caltran_utils.prepare_data(A,B,dataAmatchcol,dataBmatchcol)

        

        #prepare for cross validation
        uniquevals = np.unique(A_mean[('meta',dataAmatchcol)])
        cv_results = pd.DataFrame()
        ind = 0

        for params in paramgrid: #step through all the different permutations
            print(params)
            transformed_datakey = datakeyA + '-' + str(params)
            for key in params.keys():  # store parameters in the results file
                cv_results.loc[ind, key] = params[key]
            ct_obj = cal_tran.cal_tran(params) #create a caltran object using the current parameters
            A_mean_transformed = copy.deepcopy(A_mean)
            A_mean_transformed['wvl'] = A_mean_transformed['wvl']*0
            rmses = []
            for val in uniquevals:  #hold out each unique spectrum in turn
                print(val)
                # define the validation data (the held out spectrum)
                # and the training data (the spectra that are not held out)
                # for both data sets
                val_data_A = np.squeeze(np.array(A_mean[A_mean[('meta', dataAmatchcol)] == val]['wvl'],dtype='float'))
                train_data_A = np.squeeze(np.array(A_mean[A_mean[('meta', dataAmatchcol)] != val]['wvl'],dtype='float'))
                val_data_B = np.squeeze(np.array(B_mean[B_mean[('meta', dataBmatchcol)] == val]['wvl'],dtype='float'))
                train_data_B = np.squeeze(np.array(B_mean[B_mean[('meta', dataBmatchcol)] != val]['wvl'],dtype='float'))

                ct_obj.derive_transform(train_data_A,train_data_B) #derive the transform based on the training data
                val_data_A_transformed = ct_obj.apply_transform(val_data_A) #apply the transform to the held out spectrum from A

                if self.keep_spectra_checkBox.isChecked():
                    A_mean_transformed.loc[A_mean_transformed[('meta', dataAmatchcol)] == val, 'wvl'] = val_data_A_transformed #this step is very slow, can we speed it up?
                rmses.append(mismatch_rmse(val_data_A_transformed,val_data_B))
                cv_results.loc[ind, val + '_RMSE'] = rmses[-1] #record the RMSE for the held out spectrum
            cv_results.loc[ind,'average_RMSE']=np.mean(rmses)
            if self.keep_spectra_checkBox.isChecked():
                Modules.data_count += 1
                self.index = Modules.data_count
                self.list_amend(self.datakeys,self.index,transformed_datakey)
                self.data[transformed_datakey] = spectral_data.spectral_data(A_mean_transformed)
            ind = ind + 1
        cv_results.columns = pd.MultiIndex.from_tuples([('cv', col) for col in cv_results.columns])

        cvid = 'Caltran CV Results'
        number = 1
        while cvid in self.datakeys:
            number += 1
            cvid = cvid + ' - ' + str(number)

        Modules.data_count += 1
        self.index = Modules.data_count
        self.list_amend(self.datakeys,self.index,cvid)
        self.data[cvid] = cv_results


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    Form = QtWidgets.QWidget()
    ui = CalibrationTransferCV()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
