from PyQt5 import QtWidgets

from point_spectra_gui.ui.RegressionPredict import Ui_Form
from point_spectra_gui.util.Modules import Modules


class RegressionPredict(Ui_Form, Modules):

    def __init__(self):
        self.predict_count = len(self.predictkeys)

    def delete(self):
        pass

    def setupUi(self, Form):
        super().setupUi(Form)
        Modules.setupUi(self, Form)

    def get_widget(self):
        return self.formGroupBox

    def connectWidgets(self, setup=False):
        self.changeComboListVars(self.chooseDataListWidget, self.datakeys)
        self.setComboBox(self.chooseModelComboBox, self.modelkeys)
        self.chooseDataListWidget.itemSelectionChanged.connect(lambda: self.setComboBox(self.chooseModelComboBox, self.modelkeys))

    def run(self):
        datakeys = [str(i.text()) for i in self.chooseDataListWidget.selectedItems()]
        modelkey = self.chooseModelComboBox.currentText()
        try:
            for datakey in datakeys:
                print('Predicting '+datakey)
                x_var_tmp = self.model_xvars[modelkey]
                data_tmp = self.data[datakey].df[x_var_tmp]
                data_tmp.fillna(value=0, inplace=True)
                if self.data[datakey].df[x_var_tmp].shape[1] != self.models[modelkey].model.coef_.shape[0]:
                    print("Warning: Size of input dataframe does not match size of validation dataset.")
                prediction = self.models[modelkey].predict(data_tmp)
                predictname = ('predict', modelkey + ' - ' + datakey + ' - Predict')
                self.data[datakey].df[predictname] = prediction
        except Exception as e:
            print(e)



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    Form = QtWidgets.QWidget()
    ui = RegressionPredict()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
