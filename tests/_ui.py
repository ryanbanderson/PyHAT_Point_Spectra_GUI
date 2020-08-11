import sys
import time
import warnings

from point_spectra_gui import core

try:
    import qtmodern.styles

    q = True
except:
    q = False
    warnings.warn("You're missing the qtmodern package."
                  "to install it use pip install qtmodern")

from PyQt5 import QtWidgets

from point_spectra_gui.core.MainWindow import MainWindow


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
        return result

    return timed


class Ui_MainWindow(MainWindow):
    @timeit
    def connectWidgets(self):
        """
        Connect all the widgets associated with the MainWindow UI
        :return:
        """
        super().connectWidgets()
        self.addWidget(core.ReadChemCamData.ReadChemCamData)
        self.addWidget(core.BaselineRemoval.BaselineRemoval)
        self.addWidget(core.CrossValidation.CrossValidation)
        self.addWidget(core.DimensionalityReduction.DimensionalityReduction)
        self.addWidget(core.Clustering.Clustering)
        self.addWidget(core.Resample.Interpolation)
        self.addWidget(core.LoadData.LoadData)
        self.addWidget(core.WriteToCSV.WriteToCSV)
        self.addWidget(core.RenameData.RenameData)
        self.addWidget(core.MaskData.MaskData)
        self.addWidget(core.MultiplyByVector.MultiplyByVector)
        self.addWidget(core.Normalization.Normalization)
        self.addWidget(core.OutputFolder.OutputFolder)
        self.addWidget(core.PeakAreas.PeakAreas)
        self.addWidget(core.Plot.Plot)
        self.addWidget(core.Plot_ICA_PCA.Plot_ICA_PCA)
        self.addWidget(core.PlotSpectra.PlotSpectra)
        self.addWidget(core.RegressionTrain.RegressionTrain)
        self.addWidget(core.RegressionPredict.RegressionPredict)
        self.addWidget(core.RemoveRows.RemoveRows)
        self.addWidget(core.SplitDataset.SplitDataset)
        self.addWidget(core.OutlierIdentify.OutlierRemoval)
        self.addWidget(core.StratifiedFolds.StratifiedFolds)
        self.addWidget(core.SubmodelBlend.SubmodelBlend)
        self.addWidget(core.SpecDeriv.SpecDeriv)
        self.addWidget(core.CombineDataSets.CombineDataSets)
        self.addWidget(core.RestoreTrainedModel.RestoreTrainedModel)
        self.addWidget(core.SaveTrainedModel.SaveTrainedModel)
        self.addWidget(core.SaveRegressionModel.SaveRegressionModel)


def main():
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    app.exec_()


if __name__ == '__main__':
    main()
