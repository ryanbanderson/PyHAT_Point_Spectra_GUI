import numpy as np
from PyQt5 import QtWidgets
import pandas as pd
from point_spectra_gui.ui.PeakAreas import Ui_Form
from point_spectra_gui.util.Modules import Modules
from point_spectra_gui.util.spectral_data import spectral_data
from libpyhat.transform.peak_area import peak_area

class PeakAreas(Ui_Form, Modules):
    def setupUi(self, Form):
        super().setupUi(Form)
        Modules.setupUi(self, Form)

    def get_widget(self):
        return self.groupBox

    def connectWidgets(self):
        self.peakMinimaLineEdit.setText("None (calculate from average spectrum)")
        self.setComboBox(self.chooseDataComboBox, self.datakeys)
        self.pushButton.clicked.connect(lambda: self.on_getDataButton_clicked(self.peakMinimaLineEdit))


    def run(self):
        datakey = self.chooseDataComboBox.currentText()
        peaks_mins_file = self.peakMinimaLineEdit.text()
        if peaks_mins_file == "None (calculate from average spectrum)":
            peaks_mins_file = None

        try:
            self.data[datakey].peak_area(peaks_mins_file)
            print("Peak Areas Calculated")
            output = pd.DataFrame(columns = ['type','wvl'])
            types = np.hstack((np.repeat('peak',len(self.data[datakey].peaks)), np.repeat('min',len(self.data[datakey].mins))))
            wvls = np.hstack((self.data[datakey].peaks,self.data[datakey].mins))
            output['type']=types
            output['wvl']=wvls
            output.sort_values('wvl',axis=0,inplace=True)
            output.reset_index(inplace=True,drop=True)
            output.to_csv(self.outpath+r'/peaks_mins.csv')
            print('Peaks and mins saved to '+self.outpath+'/peaks_mins.csv')

        except Exception as e:
             print(e)

    def on_getDataButton_clicked(self, lineEdit):
        filename, _filter = QtWidgets.QFileDialog.getOpenFileName(None, "Open peaks and minima File", '.', "(*.csv)")
        lineEdit.setText(filename)
        if lineEdit.text() == "":
            lineEdit.setText("None (calculate from average spectrum)")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    Form = QtWidgets.QWidget()
    ui = PeakAreas()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
