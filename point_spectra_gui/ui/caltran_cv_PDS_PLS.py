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
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.winsize_min_spinBox = QtWidgets.QSpinBox(self.formGroupBox)
        self.winsize_min_spinBox.setMinimum(1)
        self.winsize_min_spinBox.setSingleStep(2)
        self.winsize_min_spinBox.setProperty("value", 1)
        self.winsize_min_spinBox.setObjectName("winsize_min_spinBox")
        self.horizontalLayout.addWidget(self.winsize_min_spinBox)
        self.label = QtWidgets.QLabel(self.formGroupBox)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.winsize_max_spinBox = QtWidgets.QSpinBox(self.formGroupBox)
        self.winsize_max_spinBox.setSingleStep(2)
        self.winsize_max_spinBox.setProperty("value", 9)
        self.winsize_max_spinBox.setObjectName("winsize_max_spinBox")
        self.horizontalLayout.addWidget(self.winsize_max_spinBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.formLayout.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.pls_nc_label = QtWidgets.QLabel(self.formGroupBox)
        self.pls_nc_label.setObjectName("pls_nc_label")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.pls_nc_label)
        self.pls_nc_lineEdit = QtWidgets.QLineEdit(self.formGroupBox)
        self.pls_nc_lineEdit.setObjectName("pls_nc_lineEdit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.pls_nc_lineEdit)
        self.verticalLayout.addWidget(self.formGroupBox)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(("Form"))
        self.formGroupBox.setTitle(("PDS using Partial Least Squares"))
        self.winsize_label.setText(("Window sizes from"))
        self.label.setText(("to"))
        self.pls_nc_label.setText(("# of components"))
        self.pls_nc_lineEdit.setText(("1,2,3,4,5,6,7,8,9,10"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

