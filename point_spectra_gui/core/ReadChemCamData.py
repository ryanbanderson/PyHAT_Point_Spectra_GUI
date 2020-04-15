import pandas as pd
from PyQt5 import QtWidgets
from point_spectra_gui.ui.ReadChemCamData import Ui_Form
from point_spectra_gui.util.Modules import Modules
from point_spectra_gui.util.spectral_data import spectral_data
from point_spectra_gui.util.io import io_ccam_pds
from point_spectra_gui.core.LoadData import LoadData

class ReadChemCamData(Ui_Form, Modules):
    def __init__(self):
        self.Loader = LoadData()

    def delete(self):
        self.Loader.delete()

    def setupUi(self, Form):
        super().setupUi(Form)
        Modules.setupUi(self, Form)

    def get_widget(self):
        return self.groupBox

    def connectWidgets(self):
        self.searchDirectorypushButton.clicked.connect(self.on_searchpathButton_clicked)
        self.metadatapushButton.clicked.connect(self.on_metadataButton_clicked)


    def on_searchpathButton_clicked(self):
        dirname = QtWidgets.QFileDialog.getExistingDirectory(parent=None, caption="Select Search Directory",
                                                             directory='.')
        self.searchDirectoryLineEdit.setText(dirname)
        if self.searchDirectoryLineEdit.text() == "":
            self.searchDirectoryLineEdit.setText("*/")

    def on_metadataButton_clicked(self):
        self.metadata_file, null = QtWidgets.QFileDialog.getOpenFileNames(parent=None,
                                                                          caption="Select metadata file(s)",
                                                                          directory='.')
        self.metadataFilesLineEdit.setText(str(self.metadata_file))
        if self.metadataFilesLineEdit.text() == "":
            self.metadataFilesLineEdit.setText("*/")


    def run(self):
        searchdir = self.searchDirectoryLineEdit.text()
        searchstring = self.searchStringLineEdit.text()
        to_csv = self.outputFileNameLineEdit.text()
        left_on = self.data_col.text()
        right_on = self.lookup_col.text()
        keyname = self.lineEdit.text()
        try:
            lookupfile = self.metadataFilesLineEdit.text()
            lookupfile = lookupfile[2:-2].split(',')
            lookupfile = [f.strip('\\\' "') for f in lookupfile]
            if lookupfile[0] == '':
                lookupfile = None
        except:
            lookupfile = None
        ave = self.averagesradioButton.isChecked()
        io_ccam_pds.ccam_batch(searchdir, searchstring=searchstring, to_csv=Modules.outpath + '/' + to_csv,
                               lookupfile=lookupfile, ave=ave, left_on=left_on,
                               right_on=right_on)

        self.Loader.run(filename=Modules.outpath + '/' + to_csv, keyname=keyname)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    Form = QtWidgets.QWidget()
    ui = ReadChemCamData()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
