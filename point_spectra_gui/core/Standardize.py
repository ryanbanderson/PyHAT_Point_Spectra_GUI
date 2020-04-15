import numpy as np
from PyQt5 import QtWidgets
import pandas as pd
from point_spectra_gui.ui.Standardize import Ui_Form
from point_spectra_gui.util.Modules import Modules
from sklearn.preprocessing import StandardScaler
from point_spectra_gui.util.spectral_data import spectral_data

class Standardize(Ui_Form, Modules):
    def setupUi(self, Form):
        super().setupUi(Form)
        Modules.setupUi(self, Form)

    def get_widget(self):
        return self.groupBox

    def connectWidgets(self):
        self.setComboBox(self.chooseDataComboBox, self.datakeys)
        self.setComboBox(self.comboBox, self.datakeys)

    def run(self):
        if 'Standardization Vectors' in self.datakeys:
            pass
        else:
            Modules.data_count += 1
            self.list_amend(self.datakeys, Modules.data_count, 'Standardization Vectors')

        datakey_to_scale = self.chooseDataComboBox.currentText()
        datakey_to_fit = self.comboBox.currentText()

        try:
            scaler = StandardScaler()
            scaler.fit(self.data[datakey_to_fit].df['wvl'])
            self.data[datakey_to_scale].df['wvl']=scaler.transform(self.data[datakey_to_scale].df['wvl'])

            print(datakey_to_scale+ " standardized using spectral channel mean and standard deviations from "+datakey_to_fit)

            try:
                scaler_out = pd.DataFrame(np.vstack((scaler.var_,scaler.mean_)).T)
                scaler_out.index = [('wvl',x) for x in self.data[datakey_to_fit].df['wvl'].columns.values]
                scaler_out = scaler_out.T
                scaler_out[('meta', 'Dataset')] = datakey_to_fit

                try:
                    self.data['Standardization Vectors'] = spectral_data(
                        pd.concat([self.data['Standardization Vectors'].df, scaler_out]))
                except:
                    self.data['Standardization Vectors'] = spectral_data(scaler_out)

            except:
                pass

        except Exception as e:
             print(e)



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    Form = QtWidgets.QWidget()
    ui = Standardize()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
