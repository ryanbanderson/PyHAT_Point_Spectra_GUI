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
        self.ncLabel = QtWidgets.QLabel(self.formGroupBox)
        self.ncLabel.setObjectName("ncLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.ncLabel)
        self.solver_label = QtWidgets.QLabel(self.formGroupBox)
        self.solver_label.setObjectName("solver_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.solver_label)
        self.solver_comboBox = QtWidgets.QComboBox(self.formGroupBox)
        self.solver_comboBox.setObjectName("solver_comboBox")
        self.solver_comboBox.addItem("")
        self.solver_comboBox.addItem("")
        self.solver_comboBox.addItem("")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.solver_comboBox)
        self.nc_spinBox = QtWidgets.QSpinBox(self.formGroupBox)
        self.nc_spinBox.setObjectName("nc_spinBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.nc_spinBox)
        self.shrinkage_checkBox = QtWidgets.QCheckBox(self.formGroupBox)
        self.shrinkage_checkBox.setObjectName("shrinkage_checkBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.shrinkage_checkBox)
        self.verticalLayout.addWidget(self.formGroupBox)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(("Form"))
        self.ncLabel.setText(("Num of Components"))
        self.solver_label.setText(("Solver"))
        self.solver_comboBox.setItemText(0, ("Singular Value Decomposition"))
        self.solver_comboBox.setItemText(1, ("Least Squares"))
        self.solver_comboBox.setItemText(2, ("Eigenvalue"))
        self.shrinkage_checkBox.setText(("Shrinkage"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())