# -*- coding: utf-8 -*-

# Automatically generated - don't edit.
# Use `python setup.py build_ui` to update it.

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formGroupBox = QtWidgets.QGroupBox(Form)
        self.formGroupBox.setObjectName("formGroupBox")
        self.formLayout = QtWidgets.QFormLayout(self.formGroupBox)
        self.formLayout.setObjectName("formLayout")
        self.winsize_label = QtWidgets.QLabel(self.formGroupBox)
        self.winsize_label.setObjectName("winsize_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.winsize_label)
        self.pls_nc_label = QtWidgets.QLabel(self.formGroupBox)
        self.pls_nc_label.setObjectName("pls_nc_label")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.pls_nc_label)
        self.winsize_spin = QtWidgets.QSpinBox(self.formGroupBox)
        self.winsize_spin.setMinimum(1)
        self.winsize_spin.setSingleStep(2)
        self.winsize_spin.setProperty("value", 1)
        self.winsize_spin.setObjectName("winsize_spin")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.winsize_spin)
        self.nc_spin = QtWidgets.QSpinBox(self.formGroupBox)
        self.nc_spin.setMinimum(1)
        self.nc_spin.setObjectName("nc_spin")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.nc_spin)
        self.verticalLayout.addWidget(self.formGroupBox)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(("Form"))
        self.formGroupBox.setTitle(("PDS using Partial Least Squares"))
        self.winsize_label.setText(("Window size"))
        self.pls_nc_label.setText(("# of components"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

