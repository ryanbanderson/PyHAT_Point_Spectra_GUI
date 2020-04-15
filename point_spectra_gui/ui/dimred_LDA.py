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
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.nc_label = QtWidgets.QLabel(self.groupBox)
        self.nc_label.setObjectName("nc_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.nc_label)
        self.nc_spin = QtWidgets.QSpinBox(self.groupBox)
        self.nc_spin.setObjectName("nc_spin")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.nc_spin)
        self.class_label = QtWidgets.QLabel(self.groupBox)
        self.class_label.setObjectName("class_label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.class_label)
        self.class_combo = QtWidgets.QComboBox(self.groupBox)
        self.class_combo.setObjectName("class_combo")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.class_combo)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.comboBox = QtWidgets.QComboBox(self.groupBox)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.comboBox)
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(("Form"))
        self.nc_label.setText(("# of components"))
        self.class_label.setText(("Class column"))
        self.label.setText(("Solver"))
        self.comboBox.setItemText(0, ("Singular Value Decomposition"))
        self.comboBox.setItemText(1, ("Eigenvalue"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())