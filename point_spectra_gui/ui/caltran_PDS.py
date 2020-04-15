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
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.LabelRole, self.horizontalLayout)
        self.pls_spin = QtWidgets.QSpinBox(self.formGroupBox)
        self.pls_spin.setMaximum(4)
        self.pls_spin.setProperty("value", 1)
        self.pls_spin.setObjectName("pls_spin")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.pls_spin)
        self.winsize_spin = QtWidgets.QSpinBox(self.formGroupBox)
        self.winsize_spin.setSingleStep(2)
        self.winsize_spin.setProperty("value", 5)
        self.winsize_spin.setObjectName("winsize_spin")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.winsize_spin)
        self.winsize_label = QtWidgets.QLabel(self.formGroupBox)
        self.winsize_label.setObjectName("winsize_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.winsize_label)
        self.pls_checkbox = QtWidgets.QCheckBox(self.formGroupBox)
        self.pls_checkbox.setObjectName("pls_checkbox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.pls_checkbox)
        self.pls_nc_label = QtWidgets.QLabel(self.formGroupBox)
        self.pls_nc_label.setObjectName("pls_nc_label")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.pls_nc_label)
        self.verticalLayout.addWidget(self.formGroupBox)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(("Form"))
        self.formGroupBox.setTitle(("PDS - Piecewise Direct Standardization"))
        self.winsize_label.setText(("Window size:"))
        self.pls_checkbox.setText(("PLS"))
        self.pls_nc_label.setText(("# of components"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

