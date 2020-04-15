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
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.fit_interceptLabel = QtWidgets.QLabel(self.formGroupBox)
        self.fit_interceptLabel.setObjectName("fit_interceptLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.fit_interceptLabel)
        self.fit_intercept_listWidget = QtWidgets.QListWidget(self.formGroupBox)
        self.fit_intercept_listWidget.setMaximumSize(QtCore.QSize(16777215, 50))
        self.fit_intercept_listWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.fit_intercept_listWidget.setObjectName("fit_intercept_listWidget")
        item = QtWidgets.QListWidgetItem()
        self.fit_intercept_listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.fit_intercept_listWidget.addItem(item)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.fit_intercept_listWidget)
        self.normalizeLabel = QtWidgets.QLabel(self.formGroupBox)
        self.normalizeLabel.setObjectName("normalizeLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.normalizeLabel)
        self.normalize_list = QtWidgets.QListWidget(self.formGroupBox)
        self.normalize_list.setMaximumSize(QtCore.QSize(16777215, 50))
        self.normalize_list.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.normalize_list.setObjectName("normalize_list")
        item = QtWidgets.QListWidgetItem()
        self.normalize_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.normalize_list.addItem(item)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.normalize_list)
        self.n_nonzero_coefsLabel = QtWidgets.QLabel(self.formGroupBox)
        self.n_nonzero_coefsLabel.setObjectName("n_nonzero_coefsLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.n_nonzero_coefsLabel)
        self.n_nonzero_coefsLineEdit = QtWidgets.QLineEdit(self.formGroupBox)
        self.n_nonzero_coefsLineEdit.setObjectName("n_nonzero_coefsLineEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.n_nonzero_coefsLineEdit)
        self.verticalLayout.addWidget(self.formGroupBox)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(("Form"))
        self.formGroupBox.setToolTip(("<html><head/><body><p>Least-angle regression (LARS) is a regression algorithm for high-dimensional data, developed by Bradley Efron, Trevor Hastie, Iain Johnstone and Robert Tibshirani. LARS is similar to forward stepwise regression. At each step, it finds the predictor most correlated with the response. When there are multiple predictors having equal correlation, instead of continuing along the same predictor, it proceeds in a direction equiangular between the predictors.</p><p><span style=\" font-weight:600;\">The advantages of LARS are:</span></p><p>It is numerically efficient in contexts where p &gt;&gt; n (i.e., when the number of dimensions is significantly greater than the number of points)</p><p>It is computationally just as fast as forward selection and has the same order of complexity as an ordinary least squares.</p><p>It produces a full piecewise linear solution path, which is useful in cross-validation or similar attempts to tune the model.</p><p>If two variables are almost equally correlated with the response, then their coefficients should increase at approximately the same rate. The algorithm thus behaves as intuition would expect, and also is more stable.</p><p>It is easily modified to produce solutions for other estimators, like the Lasso.</p><p><span style=\" font-weight:600;\">The disadvantages of the LARS method include:</span></p><p>Because LARS is based upon an iterative refitting of the residuals, it would appear to be especially sensitive to the effects of noise. This problem is discussed in detail by Weisberg in the discussion section of the Efron et al. (2004) Annals of Statistics article.</p></body></html>"))
        self.fit_interceptLabel.setText(("Fit Intercept"))
        __sortingEnabled = self.fit_intercept_listWidget.isSortingEnabled()
        self.fit_intercept_listWidget.setSortingEnabled(False)
        item = self.fit_intercept_listWidget.item(0)
        item.setText(("True"))
        item = self.fit_intercept_listWidget.item(1)
        item.setText(("False"))
        self.fit_intercept_listWidget.setSortingEnabled(__sortingEnabled)
        self.normalizeLabel.setText(("Normalize"))
        __sortingEnabled = self.normalize_list.isSortingEnabled()
        self.normalize_list.setSortingEnabled(False)
        item = self.normalize_list.item(0)
        item.setText(("True"))
        item = self.normalize_list.item(1)
        item.setText(("False"))
        self.normalize_list.setSortingEnabled(__sortingEnabled)
        self.n_nonzero_coefsLabel.setText(("# of coefficients"))
        self.n_nonzero_coefsLineEdit.setText(("500"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
