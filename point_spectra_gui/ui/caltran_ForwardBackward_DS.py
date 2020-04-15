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
        self.formGroupBox.setTitle("")
        self.formGroupBox.setObjectName("formGroupBox")
        self.formLayout = QtWidgets.QFormLayout(self.formGroupBox)
        self.formLayout.setObjectName("formLayout")
        self.t_label = QtWidgets.QLabel(self.formGroupBox)
        self.t_label.setObjectName("t_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.t_label)
        self.svt_label = QtWidgets.QLabel(self.formGroupBox)
        self.svt_label.setObjectName("svt_label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.svt_label)
        self.L1_label = QtWidgets.QLabel(self.formGroupBox)
        self.L1_label.setObjectName("L1_label")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.L1_label)
        self.epsilon_label = QtWidgets.QLabel(self.formGroupBox)
        self.epsilon_label.setObjectName("epsilon_label")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.epsilon_label)
        self.niter_spinBox = QtWidgets.QSpinBox(self.formGroupBox)
        self.niter_spinBox.setMinimum(1)
        self.niter_spinBox.setProperty("value", 50)
        self.niter_spinBox.setDisplayIntegerBase(20)
        self.niter_spinBox.setObjectName("niter_spinBox")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.niter_spinBox)
        self.niter_label = QtWidgets.QLabel(self.formGroupBox)
        self.niter_label.setObjectName("niter_label")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.niter_label)
        self.t_spin = QtWidgets.QDoubleSpinBox(self.formGroupBox)
        self.t_spin.setDecimals(6)
        self.t_spin.setSingleStep(0.0001)
        self.t_spin.setProperty("value", 0.001)
        self.t_spin.setObjectName("t_spin")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.t_spin)
        self.svt_spin = QtWidgets.QDoubleSpinBox(self.formGroupBox)
        self.svt_spin.setDecimals(3)
        self.svt_spin.setSingleStep(0.01)
        self.svt_spin.setProperty("value", 1.0)
        self.svt_spin.setObjectName("svt_spin")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.svt_spin)
        self.L1_spin = QtWidgets.QDoubleSpinBox(self.formGroupBox)
        self.L1_spin.setDecimals(3)
        self.L1_spin.setSingleStep(0.01)
        self.L1_spin.setProperty("value", 1.0)
        self.L1_spin.setObjectName("L1_spin")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.L1_spin)
        self.epsilon_spin = QtWidgets.QDoubleSpinBox(self.formGroupBox)
        self.epsilon_spin.setDecimals(5)
        self.epsilon_spin.setSingleStep(1e-05)
        self.epsilon_spin.setProperty("value", 1e-05)
        self.epsilon_spin.setObjectName("epsilon_spin")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.epsilon_spin)
        self.verticalLayout.addWidget(self.formGroupBox)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(("Form"))
        self.t_label.setText(("t"))
        self.svt_label.setText(("svt"))
        self.L1_label.setText(("L1"))
        self.epsilon_label.setText(("Epsilon"))
        self.niter_label.setText(("# of iterations"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

