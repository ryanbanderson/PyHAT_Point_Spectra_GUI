from PyQt5 import QtWidgets

from point_spectra_gui.ui.Resample import Ui_Form
from point_spectra_gui.util.Modules import Modules

class Resample(Ui_Form, Modules):
    """
    Interpolates two datasets
    """

    def setupUi(self, Form):
        super().setupUi(Form)
        Modules.setupUi(self, Form)

    def get_widget(self):
        return self.formGroupBox

    def connectWidgets(self):
        self.setComboBox(self.resampleDataComboBox, self.datakeys)
        self.setComboBox(self.referenceDataComboBox, self.datakeys)

    def run(self):
        datakey_to_interp = self.resampleDataComboBox.currentText()
        datakey_ref = self.referenceDataComboBox.currentText()
        print(self.data[datakey_ref].df.columns.levels[0])
        self.data[datakey_to_interp].interp(self.data[datakey_ref].df['wvl'].columns)
        nan_cols = self.data[datakey_to_interp].df['wvl'].columns[self.data[datakey_to_interp].df['wvl'].isna().any()]
        print('Dropping the following wavelengths (no data):')
        for i in nan_cols:
            print(str(i))
        nan_cols = [('wvl',i) for i in nan_cols]

        self.data[datakey_to_interp].df = self.data[datakey_to_interp].df.drop(nan_cols,axis=1)
        self.data[datakey_ref].df = self.data[datakey_ref].df.drop(nan_cols,axis=1)
        pass


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    Form = QtWidgets.QWidget()
    ui = Resample()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
