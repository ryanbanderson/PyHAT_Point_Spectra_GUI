import pandas as pd
from PyQt5 import QtWidgets

from point_spectra_gui.ui.CombineDataSets import Ui_Form
from point_spectra_gui.util.Modules import Modules
from point_spectra_gui.util.spectral_data import spectral_data

class CombineDataSets(Ui_Form, Modules):

    def setupUi(self, Form):
        self.Form = Form
        super().setupUi(Form)
        Modules.setupUi(self, Form)

    def get_widget(self):
        return self.formGroupBox

    def connectWidgets(self):
        self.setComboBox(self.dataSet1ComboBox, self.datakeys)
        self.setComboBox(self.dataSet2ComboBox, self.datakeys)

    def run(self):
        Modules.data_count += 1
        self.count = Modules.data_count
        dataSet1 = self.dataSet1ComboBox.currentText()
        dataSet2 = self.dataSet2ComboBox.currentText()
        newkey = self.outputToDataSetLineEdit.text()
        if newkey != '':
            self.list_amend(self.datakeys, self.count, newkey)
            try:
                data1 = self.data[dataSet1].df
                data2 = self.data[dataSet2].df
                data1[('meta','Dataset')] = dataSet1
                data2[('meta', 'Dataset')] = dataSet2
                newdata = spectral_data(pd.concat([data1, data2], ignore_index=True))
                self.data[newkey] = newdata
            except:
                pass


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
