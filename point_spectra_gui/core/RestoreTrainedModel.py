import pickle

from PyQt5 import QtWidgets, QtGui

from point_spectra_gui.ui.RestoreTrainedModel import Ui_Form
from point_spectra_gui.util.Modules import Modules


class RestoreTrainedModel(Ui_Form, Modules):
    def setupUi(self, Form):
        super().setupUi(Form)
        Modules.setupUi(self, Form)

    def get_widget(self):
        return self.groupBox

    def connectWidgets(self):
        self.retorePushButton.clicked.connect(lambda: self.on_restorePushButton_clicked(self.restoreLineEdit))

    def run(self):
        # load pickled data
        filename = self.restoreLineEdit.text()
        with open(filename, 'rb') as fp:
            load = pickle.load(fp)
        self.modelkeys.append(load[0])
        self.models[load[0]] = load[1]
        self.model_xvars[load[0]]=load[2]
        self.model_yvars[load[0]] = load[3]

        pass

    def on_restorePushButton_clicked(self, lineEdit):
        # list[0] will hold the dictionary data of the UI
        # list[1] will hold the self.models data
        # load the json file into the restoreTextBrowser
        filename, _filter = QtWidgets.QFileDialog.getOpenFileName(None, "Open Data File", self.outpath, "(*.tram)")
        lineEdit.setText(filename)
        if lineEdit.text() == "":
            lineEdit.setText("*.tram")
        # Load the json file into the restoreTextBrowser to be viewed
        with open(filename, 'rb') as fp:
            output = pickle.load(fp)
            print('Model name: '+output[0])
            print('x variable: '+output[2][0])





if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = RestoreTrainedModel()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
