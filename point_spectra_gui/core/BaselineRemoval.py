from PyQt5 import QtWidgets
from point_spectra_gui.util.spectral_data import spectral_data
from libpyhat.transform.remove_baseline import remove_baseline
from point_spectra_gui.util import Qtickle
from point_spectra_gui.core.baselineRemovalMethods import *
from point_spectra_gui.ui.BaselineRemoval import Ui_Form
from point_spectra_gui.util.Modules import Modules


class BaselineRemoval(Ui_Form, Modules):
    def setupUi(self, Form):
        self.Form = Form
        super().setupUi(Form)
        Modules.setupUi(self, Form)
        self.baselineMethods()

    def get_widget(self):
        return self.formGroupBox

    def make_regression_widget(self, alg, params=None):
        self.hideAll()
        print(alg)
        for i in range(len(self.chooseAlgorithmList)):
            if alg == self.chooseAlgorithmList[i] and i > 0:
                self.alg[i - 1].setHidden(False)

    def connectWidgets(self):
        self.chooseAlgorithmList = ['Choose an algorithm',
                                    'AirPLS',
                                    'ALS',
                                    'Dietrich',
                                    'FABC',
                                    'KK',
                                    'Median',
                                    'Polyfit',
                                    'Rubberband',
                                    'Wavelet a Trous + Spline',
                                    'Min + Interpolate'
                                    ]
        self.setComboBox(self.chooseDataComboBox, self.datakeys)
        self.setComboBox(self.chooseAlgorithmComboBox, self.chooseAlgorithmList)
        self.chooseAlgorithmComboBox.currentIndexChanged.connect(
            lambda: self.make_regression_widget(self.chooseAlgorithmComboBox.currentText()))

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

    def run(self):
        Modules.data_count += 1
        self.baseline_index = Modules.data_count
        Modules.data_count += 1
        self.baseline_removed_index = Modules.data_count

        method = self.chooseAlgorithmComboBox.currentText()
        datakey = self.chooseDataComboBox.currentText()
        # return method parameters and parameters that changed
        methodParameters, _changed = self.getMethodParams(self.chooseAlgorithmComboBox.currentIndex())

        datakey_new = datakey + '-Baseline Removed-' + method + str(_changed)
        datakey_baseline = datakey + '-Baseline-' + method + str(_changed)
        self.list_amend(self.datakeys, self.baseline_index, datakey_baseline)
        self.list_amend(self.datakeys, self.baseline_removed_index, datakey_new)
        self.data[datakey_new] = self.data[datakey].df.copy(deep=True)
        df, df_baseline = remove_baseline(self.data[datakey_new],method, segment=True, params=methodParameters)
        self.data[datakey_new] = spectral_data(df)
        self.data[datakey_baseline] = spectral_data(df_baseline)

    def hideAll(self):
        for a in self.alg:
            a.setHidden(True)

    def getMethodParams(self, index):
        return self.alg[index - 1].run()

    def baselineMethods(self):
        self.alg = []
        list_forms = [
            AirPLS,
            ALS,
            Dietrich,
            FABC,
            KK,
            Median,
            Polyfit,
            Rubberband,
            WaveletSpline,
            MinInterp
        ]
        for items in list_forms:
            self.alg.append(items.Ui_Form())
            self.alg[-1].setupUi(self.Form)
            self.algorithmLayout.addWidget(self.alg[-1].get_widget())
            self.alg[-1].setHidden(True)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = BaselineRemoval()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
