from PyQt5 import QtWidgets

from point_spectra_gui.util import Qtickle
from point_spectra_gui.core.outlierRemovalMethods import *
from point_spectra_gui.ui.OutlierRemoval import Ui_Form
from point_spectra_gui.util.Modules import Modules
from libpyhat.utils.outlier_removal import outlier_removal
from point_spectra_gui.util.spectral_data import spectral_data

class OutlierRemoval(Ui_Form, Modules):
    def setupUi(self, Form):
        self.Form = Form
        super().setupUi(Form)
        Modules.setupUi(self, Form)
        self.outlierRemovalMethods()

    def get_widget(self):
        return self.groupLayout

    def make_outlier_widget(self, alg, params=None):
        self.hideAll()
        print(alg)
        for i in range(1,len(self.algorithm_list)):
            if alg == self.algorithm_list[i]:
                self.alg[i - 1].setHidden(False)

    def connectWidgets(self, setup=False):
        self.algorithm_list = ['Choose an algorithm',
                               'Isolation Forest',
                               'Local Outlier Factor'
                               ]

        self.setComboBox(self.chooseDataComboBox, self.datakeys)
        self.setComboBox(self.chooseAlgorithmComboBox, self.algorithm_list)
        self.changeComboListVars(self.xVariableList, self.xvar_choices())
        if setup==False:
            self.chooseAlgorithmComboBox.currentIndexChanged.connect(
                lambda: self.make_outlier_widget(self.chooseAlgorithmComboBox.currentText()))
            self.chooseDataComboBox.currentIndexChanged.connect(
                lambda: self.changeComboListVars(self.xVariableList, self.xvar_choices()))

    def getGuiParams(self):
        """
        Overriding Modules' getGuiParams, because I'll need to do a list of lists
        in order to obtain the regressionMethods' parameters
        """
        self.qt = Qtickle.Qtickle(self)
        s = []
        s.append(self.qt.guiSave())
        for items in self.alg:
            s.append(items.getGuiParams())
        return s

    def setGuiParams(self, dict):
        self.qt = Qtickle.Qtickle(self)
        self.qt.guiRestore(dict[0])
        for i in range(len(dict)):
            self.alg[i - 1].setGuiParams(dict[i])

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
        for i in range(len(dict)):
            self.alg[i - 1].selectiveSetGuiParams(dict[i])


    def run(self):
        method = self.chooseAlgorithmComboBox.currentText()
        datakey = self.chooseDataComboBox.currentText()
        xvars = [str(x.text()) for x in self.xVariableList.selectedItems()]
        params, modelkey = self.getMethodParams(self.chooseAlgorithmComboBox.currentIndex())
        self.data[datakey].outlier_removal(xvars, method, params)

    def xvar_choices(self):
        try:
            xvarchoices = self.data[self.chooseDataComboBox.currentText()].df.columns.levels[0].values
            xvarchoices = [i for i in xvarchoices if not 'Unnamed' in i]  # remove unnamed columns from choices
        except:
            xvarchoices = ['No valid choices!']
        return xvarchoices

    def hideAll(self):
        for a in self.alg:
            a.setHidden(True)

    def getMethodParams(self, index):
        return self.alg[index - 1].run()

    def outlierRemovalMethods(self):
        self.alg = []
        list_forms = [outliers_IsolationForest,
                      outliers_LOF]
        for items in list_forms:
            self.alg.append(items.Ui_Form())
            self.alg[-1].setupUi(self.Form)
            self.algorithmLayout.addWidget(self.alg[-1].get_widget())
            self.alg[-1].setHidden(True)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = OutlierRemoval()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
