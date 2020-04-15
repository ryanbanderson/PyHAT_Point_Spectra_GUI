import numpy as np
import pandas as pd
from PyQt5 import QtWidgets
from point_spectra_gui.util import Qtickle
from libpyhat.regression import regression
from point_spectra_gui.util.spectral_data import spectral_data
from point_spectra_gui.core.regressionMethods import *
from point_spectra_gui.ui.RegressionTrain import Ui_Form
from point_spectra_gui.util.Modules import Modules


class RegressionTrain(Ui_Form, Modules):

    def setupUi(self, Form):
        self.Form = Form
        super().setupUi(Form)
        Modules.setupUi(self, Form)
        self.regressionMethods()

    def get_widget(self):
        return self.groupLayout

    def make_regression_widget(self, alg, params=None):
        self.hideAll()
        #print(alg)
        try:
            self.alg[alg].setHidden(False)
        except:
            pass

    def connectWidgets(self):
        self.algorithm_list = ['Choose an algorithm',
                               'PLS',
                               'OLS',
                               'OMP',
                               'LASSO',
                               'Elastic Net',
                               'Ridge',
                               'BRR',
                               'ARD',
                               'LARS',
                               # 'LASSO LARS', - This is having issues. Hide until we can debug
                               'SVR',
                               'GBR',
                               'GP']
        self.setComboBox(self.chooseAlgorithmComboBox, self.algorithm_list)
        self.setComboBox(self.chooseDataComboBox, self.datakeys)
        self.changeComboListVars(self.yVariableList, self.yvar_choices())
        self.changeComboListVars(self.xVariableList, self.xvar_choices())
        self.xvar_choices()
        self.chooseAlgorithmComboBox.currentIndexChanged.connect(
            lambda: self.make_regression_widget(self.chooseAlgorithmComboBox.currentText()))
        self.chooseDataComboBox.currentIndexChanged.connect(self.refreshLists)
        self.yVariableList.currentItemChanged.connect(self.set_yRange)

    def set_yRange(self):
        try:
            yvar = ('comp', self.yVariableList.currentItem().text())
            ymax = self.data[self.chooseDataComboBox.currentText()].df[yvar].max()
            ymin = self.data[self.chooseDataComboBox.currentText()].df[yvar].min()
            self.yMaxDoubleSpinBox.setValue(ymax)
            self.yMinDoubleSpinBox.setValue(ymin)
        except:
            print('Failed to update Y range. Selected data may be non-numeric!')

    def refreshLists(self):
        self.changeComboListVars(self.yVariableList, self.yvar_choices())
        self.changeComboListVars(self.xVariableList, self.xvar_choices())

    def getGuiParams(self):
        """
        Overriding Modules' getGuiParams, because I'll need to do a list of lists
        in order to obtain the regressionMethods' parameters
        """
        self.qt = Qtickle.Qtickle(self)
        s = []
        s.append(self.qt.guiSave())
        for items in self.alg:
            s.append(self.alg[items].getGuiParams())
        return s

    def setGuiParams(self, dict):
        """
        Overriding Modules' setGuiParams as we are using a list of lists to

        :param dict:
        :return:
        """

        self.qt = Qtickle.Qtickle(self)
        self.qt.guiRestore(dict[0])
        keys = list(self.alg.keys())
        for i in range(len(dict)):
            self.alg[keys[i - 1]].setGuiParams(dict[i])

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
            self.alg[keys[i - 1]].selectiveSetGuiParams(dict[i])


    def run(self):
        if 'Model Coefficients' in self.datakeys:
            pass
        else:
            Modules.data_count += 1
            self.list_amend(self.datakeys, Modules.data_count, 'Model Coefficients')
        Modules.model_count += 1
        self.count = Modules.model_count

        method = self.chooseAlgorithmComboBox.currentText()
        datakey = self.chooseDataComboBox.currentText()
        xvars = [str(x.text()) for x in self.xVariableList.selectedItems()]
        yvars = [('comp', str(y.text())) for y in self.yVariableList.selectedItems()]
        yrange = [self.yMinDoubleSpinBox.value(), self.yMaxDoubleSpinBox.value()]

        params, modelkey = self.alg[self.chooseAlgorithmComboBox.currentText()].run()
        modelkey = "{} - {} - ({}, {}) {}".format(method, yvars[0][-1], yrange[0], yrange[1], modelkey)
        self.list_amend(self.modelkeys, self.count, modelkey)
        self.models[modelkey] = regression.regression([method], [params])

        x = self.data[datakey].df[xvars]
        y = self.data[datakey].df[yvars]
        x = np.array(x)
        y = np.array(y)
        ymask = np.squeeze((y > yrange[0]) & (y < yrange[1]))
        y = y[ymask]
        x = x[ymask, :]
        self.models[modelkey].fit(x, y)
        self.model_xvars[modelkey] = xvars
        self.model_yvars[modelkey] = yvars
        try:
            coef = np.squeeze(self.models[modelkey].model.coef_)
            coef = pd.DataFrame(coef)
            coef.index = pd.MultiIndex.from_tuples(self.data[datakey].df[xvars].columns.values)
            coef = coef.T
            coef[('meta', 'Model')] = modelkey
            try:
                coef[('meta', 'Intercept')] = self.models[modelkey].model.intercept_
            except:
                pass
            try:
                self.data['Model Coefficients'] = spectral_data(pd.concat([self.data['Model Coefficients'].df, coef]))
            except:
                self.data['Model Coefficients'] = spectral_data(coef)

        except:
            pass

    def yvar_choices(self):
        try:
            yvarchoices = self.data[self.chooseDataComboBox.currentText()].df['comp'].columns.values
            yvarchoices = [i for i in yvarchoices if not 'Unnamed' in i]  # remove unnamed columns from choices
        except:
            yvarchoices = ['No composition columns!']
        return yvarchoices

    def xvar_choices(self):
        try:
            xvarchoices = self.data[self.chooseDataComboBox.currentText()].df.columns.levels[0].values
            xvarchoices = [i for i in xvarchoices if not 'Unnamed' in i]  # remove unnamed columns from choices
        except:
            xvarchoices = ['No valid choices!']
        return xvarchoices

    def hideAll(self):
        for a in self.alg:
            self.alg[a].setHidden(True)

    def regressionMethods(self):
        self.alg = {'ARD': ARD.Ui_Form(),
                    'BRR': BayesianRidge.Ui_Form(),
                    'Elastic Net': ElasticNet.Ui_Form(),
                    'GP': GP.Ui_Form(),
                    # 'KRR': KRR.Ui_Form(),
                    'LARS': LARS.Ui_Form(),
                    'LASSO': Lasso.Ui_Form(),
                    # 'LASSO LARS': LassoLARS.Ui_Form(),
                    'OLS': OLS.Ui_Form(),
                    'OMP': OMP.Ui_Form(),
                    'PLS': PLS.Ui_Form(),
                    'Ridge': Ridge.Ui_Form(),
                    'SVR': SVR.Ui_Form(),
                    'GBR': GBR.Ui_Form()
                    }

        for item in self.alg:
            self.alg[item].setupUi(self.Form)
            self.algorithmLayout.addWidget(self.alg[item].get_widget())
            self.alg[item].setHidden(True)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = RegressionTrain()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
