from PyQt5 import QtWidgets

from point_spectra_gui.ui.WriteToCSV import Ui_Form
from point_spectra_gui.util.Modules import Modules


class WriteToCSV(Ui_Form, Modules):
    def setupUi(self, Form):
        super().setupUi(Form)
        Modules.setupUi(self, Form)

    def get_widget(self):
        return self.groupBox

    def connectWidgets(self, setup= False):
        self.setComboBox(self.chooseDataSetComboBox, self.datakeys)
        self.setListWidget(self.variablesToWriteListWidget, self.xvar_choices())
        self.variablesToWriteListWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.update_list()
        if setup==False:
            self.chooseDataSetComboBox.currentIndexChanged.connect(self.update_list)
            self.pushButton.clicked.connect(self.on_pushButton_clicked)

    def update_list(self):
        choices = self.xvar_choices()
        self.changeComboListVars(self.variablesToWriteListWidget, choices)
        self.variablesToWriteListWidget.selectAll()

    def run(self):
        datakey = self.chooseDataSetComboBox.currentText()
        filename = self.specifyAFilenameLineEdit.text()
        selected_cols = self.variablesToWriteListWidget.selectedItems()
        cols = []
        for selection in selected_cols:
            cols.append(selection.text())
        try:
            datatemp = self.data[datakey].df[cols]
        except:
            datatemp = self.data[datakey]['cv'][cols]

        try:
            datatemp.to_csv(self.outpath + '/' + filename)
        except:
            datatemp.to_csv(filename)

    def on_pushButton_clicked(self):
        filename, _filter = QtWidgets.QFileDialog.getSaveFileName(None, "Save Data", self.outpath, "(*.csv)")
        self.specifyAFilenameLineEdit.setText(filename)
        if self.specifyAFilenameLineEdit.text() == "":
            self.specifyAFilenameLineEdit.setText("output.csv")

    def xvar_choices(self):
        try:
            try:
                xvarchoices = self.data[self.chooseDataSetComboBox.currentText()].df.columns.levels[0].values
            except:
                xvarchoices = self.data[self.chooseDataSetComboBox.currentText()].columns.values
            xvarchoices = [i for i in xvarchoices if not 'Unnamed' in i]  # remove unnamed columns from choices
        except:
            xvarchoices = ['No valid choices!']
        return xvarchoices


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    Form = QtWidgets.QWidget()
    ui = WriteToCSV()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
