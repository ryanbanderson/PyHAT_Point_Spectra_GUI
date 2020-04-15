from PyQt5 import QtWidgets

from point_spectra_gui.util import Qtickle
from point_spectra_gui.core.dimensionalityReductionMethods import *
from point_spectra_gui.ui.DimensionalityReduction import Ui_Form
from point_spectra_gui.util.Modules import Modules
from point_spectra_gui.util.spectral_data import spectral_data
from libpyhat.transform.dim_red import dim_red

class DimensionalityReduction(Ui_Form, Modules):
    def setupUi(self, Form):
        self.Form = Form
        super().setupUi(Form)
        Modules.setupUi(self, Form)
        self.dimensionalityReductionMethods()

    def get_widget(self):
        return self.formGroupBox


    def connectWidgets(self):
        self.algorithm_list = ['Choose an algorithm',
                               'PCA',
                               'FastICA',
                               'JADE-ICA',
                               't-SNE',
                               'LLE']

        self.setComboBox(self.chooseDataComboBox, self.datakeys)
        self.setComboBox(self.chooseMethodComboBox, self.algorithm_list)
        self.chooseMethodComboBox.currentIndexChanged.connect(
            lambda: self.make_dimred_widget(self.chooseMethodComboBox.currentText()))

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
        """
        Overriding Modules' setGuiParams, because we are accessing a list of lists
        And each submodule contains it's own `setGuiParams`
        """
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
        method = self.chooseMethodComboBox.currentText()
        datakey = self.chooseDataComboBox.currentText()
        # xvars = [str(x.text()) for x in self.xVariableList.selectedItems()]
        params, modelkey = self.getMethodParams(self.chooseMethodComboBox.currentIndex())
        load_fit = False
        col = 'wvl'
        df, dimred_obj = dim_red(self.data[datakey].df, col, method, [], params, load_fit)
        dimredkey = datakey+'-'+method
        self.dimredkeys.append(dimredkey)
        self.dimred[dimredkey] = dimred_obj

    def make_dimred_widget(self, alg, params=None):
        self.hideAll()
        #print(alg)
        for i in range(len(self.algorithm_list)):
            if alg == self.algorithm_list[i]:
                self.alg[i - 1].setHidden(False)

    def hideAll(self):
        for a in self.alg:
            a.setHidden(True)

    def dimensionalityReductionMethods(self):
        self.alg = []
        list_forms = [dimred_PCA,
                      dimred_FastICA,
                      dimred_JADE,
                      dimred_tSNE,
                      dimred_LLE]
        for items in list_forms:
            self.alg.append(items.Ui_Form())
            self.alg[-1].setupUi(self.Form)
            self.dim_reduction_vlayout.addWidget(self.alg[-1].get_widget())
            self.alg[-1].setHidden(True)

    def getMethodParams(self, index):
        return self.alg[index - 1].run()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    Form = QtWidgets.QWidget()
    ui = DimensionalityReduction()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
