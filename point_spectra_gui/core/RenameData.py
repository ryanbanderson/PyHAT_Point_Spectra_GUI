from PyQt5 import QtWidgets

from point_spectra_gui.ui.RenameData import Ui_Form
from point_spectra_gui.util.Modules import Modules


class RenameData(Ui_Form, Modules):
    def setupUi(self, Form):
        super().setupUi(Form)
        Modules.setupUi(self, Form)

    def get_widget(self):
        return self.groupBox

    def rename_data(self):
        new_data_name = self.toDataLineEdit.text()
        old_data_name = self.renameDataComboBox.currentText()
        if new_data_name != '':
            data_index = [i for i,x in enumerate(self.datakeys) if x==old_data_name][0] #assumes only one data set with the old name...
            self.list_amend(self.datakeys,data_index,new_data_name)
            self.data[new_data_name] = self.data[old_data_name]
            del self.data[old_data_name]

    def connectWidgets(self):
        self.setComboBox(self.renameDataComboBox, self.datakeys)

    def run(self):
        self.rename_data()

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    Form = QtWidgets.QWidget()
    ui = RenameData()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
