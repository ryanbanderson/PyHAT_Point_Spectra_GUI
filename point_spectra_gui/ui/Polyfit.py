# -*- coding: utf-8 -*-

# Automatically generated - don't edit.
# Use `python setup.py build_ui` to update it.

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.formLayout_2 = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout_2.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName("formLayout_2")
        self.orderLabel = QtWidgets.QLabel(self.groupBox)
        self.orderLabel.setObjectName("orderLabel")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.orderLabel)
        self.orderSpinBox = QtWidgets.QSpinBox(self.groupBox)
        self.orderSpinBox.setObjectName("orderSpinBox")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.orderSpinBox)
        self.numOfStandardDeviationsLabel = QtWidgets.QLabel(self.groupBox)
        self.numOfStandardDeviationsLabel.setObjectName("numOfStandardDeviationsLabel")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.numOfStandardDeviationsLabel)
        self.numOfStandardDeviationsSpinBox = QtWidgets.QSpinBox(self.groupBox)
        self.numOfStandardDeviationsSpinBox.setObjectName("numOfStandardDeviationsSpinBox")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.numOfStandardDeviationsSpinBox)
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(("Form"))
        self.orderLabel.setText(("Order"))
        self.numOfStandardDeviationsLabel.setText(("Num of Standard Deviations"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

