import numpy as np
from PyQt5 import QtWidgets

from point_spectra_gui.ui.PlotSpectra import Ui_Form
from point_spectra_gui.util.Modules import Modules
from point_spectra_gui.util.plots import make_plot
from libpyhat.utils.utils import enumerate_duplicates
from point_spectra_gui.util.spectral_data import spectral_data

class PlotSpectra(Ui_Form, Modules):
    def setupUi(self, Form):
        super().setupUi(Form)
        Modules.setupUi(self, Form)

    def get_widget(self):
        return self.groupBox

    def connectWidgets(self):
        self.newfig_checkBox.setHidden(True)
        self.setComboBox(self.chooseDataComboBox, self.datakeys)
        self.pushButton.clicked.connect(self.on_pushButton_clicked)
        fig_choices = self.figname
        fig_choices2 = ['New Figure']
        for choice in fig_choices:
            fig_choices2.append(choice)
        fig_choices = fig_choices2
        self.setComboBox(self.figname_comboBox, fig_choices)
        self.setComboBox(self.chooseDataComboBox, self.datakeys)
        self.setListWidget(self.xVariableListWidget, self.xvar_choices())
        self.plot_spect_change_vars(self.chooseColumnComboBox)
        self.plot_spect_update_list(self.chooseRowsListWidget)

        self.chooseDataComboBox.activated[int].connect(lambda: self.plot_spect_change_vars(self.chooseColumnComboBox))
        self.chooseColumnComboBox.activated[int].connect(lambda: self.plot_spect_update_list(self.chooseRowsListWidget))
        self.chooseDataComboBox.activated[int].connect(lambda: self.plot_spect_update_list(self.chooseRowsListWidget))
        self.figname_comboBox.activated[int].connect(lambda: self.newfig_check())
        self.newfig_checkBox.stateChanged.connect(lambda: self.fig_options())


        self.xVariableListWidget.itemSelectionChanged.connect(
            lambda: self.set_spect_minmax())
        self.chooseRowsListWidget.itemSelectionChanged.connect(
            lambda: self.set_spect_minmax(set_x=False))


        self.xVariableListWidget.itemSelectionChanged.connect(self.set_xTitle)
        
    def set_xTitle(self):
        try:
            self.xtitle_lineEdit.setText(self.xVariableListWidget.currentItem().text())
        except:
            pass


    def newfig_check(self):
        if self.figname_comboBox.currentText() == 'New Figure':
            self.newfig_checkBox.setChecked(True)
        else:
            self.newfig_checkBox.setChecked(False)

    def fig_options(self):
        if self.newfig_checkBox.isChecked():
            self.xminLabel.setHidden(False)
            self.xminDoubleSpinBox.setHidden(False)
            self.yminlabel.setHidden(False)
            self.yminSpinBox.setHidden(False)
            self.xtitle_label.setHidden(False)
            self.xtitle_lineEdit.setHidden(False)
            self.ymaxlabel.setHidden(False)
            self.ymaxSpinBox.setHidden(False)
            self.xmaxLabel.setHidden(False)
            self.xmaxDoubleSpinBox.setHidden(False)
            self.ytitle_label.setHidden(False)
            self.ytitle_lineEdit.setHidden(False)
            self.plotTitleLabel.setHidden(False)
            self.plotTitleLineEdit.setHidden(False)
            self.newfig_lineEdit.setHidden(False)
            self.newfig_label.setHidden(False)
        else:
            self.xminLabel.setHidden(True)
            self.xminDoubleSpinBox.setHidden(True)
            self.yminlabel.setHidden(True)
            self.yminSpinBox.setHidden(True)
            self.xtitle_label.setHidden(True)
            self.xtitle_lineEdit.setHidden(True)
            self.ymaxlabel.setHidden(True)
            self.ymaxSpinBox.setHidden(True)
            self.xmaxLabel.setHidden(True)
            self.xmaxDoubleSpinBox.setHidden(True)
            self.ytitle_label.setHidden(True)
            self.ytitle_lineEdit.setHidden(True)
            self.plotTitleLabel.setHidden(True)
            self.plotTitleLineEdit.setHidden(True)
            self.newfig_lineEdit.setHidden(True)
            self.newfig_label.setHidden(True)

    def run(self):
        one_to_one = False
        dpi = 1000
        annot_mask = None
        cmap = None
        colortitle = ''
        marker = None
        loadfig = None

        datakey = self.chooseDataComboBox.currentText()
        try:
            xcol = self.xVariableListWidget.selectedItems()[0].text()
        except:
            xcol = 'wvl'
        col = self.chooseColumnComboBox.currentText()
        try:
            row = self.chooseRowsListWidget.selectedItems()[0].text()
        except:
            row = 'None Selected'

        if self.figname_comboBox.currentText() == 'New Figure':
            figname = self.newfig_lineEdit.text()
        else:
            figname = self.figname_comboBox.currentText()
        if not figname in self.figname:
            self.figname.append(figname)
        if figname in self.figs:
            loadfig = self.figs[figname]


        title = self.plotTitleLineEdit.text()
        xtitle = self.xtitle_lineEdit.text()
        ytitle = self.ytitle_lineEdit.text()
        figfile = self.plotFilenameLineEdit.text()
        figpath, figfile = '/'.join(figfile.split('/')[:-1]), figfile.split('/')[-1]
        color = self.colorComboBox.currentText()
        alpha = self.alphaDoubleSpinBox.value()/100.0
        linewidth = self.lineWidthDoubleSpinBox.value()

        if color == 'Red':
            color = [1, 0, 0, alpha]
        elif color == 'Green':
            color = [0, 1, 0, alpha]
        elif color == 'Blue':
            color = [0, 0, 1, alpha]
        elif color == 'Cyan':
            color = [0, 1, 1, alpha]
        elif color == 'Yellow':
            color = [1, 1, 0, alpha]
        elif color == 'Magenta':
            color = [1, 0, 1, alpha]
        elif color == 'Black':
            color = [0, 0, 0, alpha]
        else:
            color = [0, 0, 0, alpha]

        line = self.lineComboBox.currentText()
        if line == 'Points (No Line)':
            linestyle = 'None'
        elif line == 'Line':
            linestyle = '-'
        elif line == 'Dashed Line':
            linestyle = '--'
        elif line == 'Dotted Line':
            linestyle = ':'
        else:
            linestyle = '-'

        xmin = self.xminDoubleSpinBox.value()
        xmax = self.xmaxDoubleSpinBox.value()
        xrange = [xmin, xmax]

        ymin = self.yminSpinBox.value()
        ymax = self.ymaxSpinBox.value()
        yrange = [ymin, ymax]

        self.data[datakey].enumerate_duplicates(col)
        data = self.data[datakey].df

        y = np.squeeze(np.array(data.loc[data[('meta', col)].isin([row])][xcol].T))
        x = np.array(data[xcol].columns.values)
        if linestyle == 'None':
            marker = 'o'

        self.figs[figname] = make_plot(x, y, figpath=figpath, figfile=figfile, xrange=xrange, yrange=yrange,
                                       xtitle=xtitle, ytitle=ytitle, title=title, one_to_one=one_to_one,
                                       dpi=dpi, color=color, annot_mask=annot_mask, cmap=cmap,
                                       colortitle=colortitle, loadfig=loadfig, marker=marker, linestyle=linestyle,
                                       linewidth=linewidth,lbl = row)

    def xvar_choices(self):
        try:
            try:
                xvarchoices = self.data[self.chooseDataComboBox.currentText()].df.columns.levels[0].values
            except:
                xvarchoices = self.data[self.chooseDataComboBox.currentText()].columns.values
            xvarchoices = [i for i in xvarchoices if not 'Unnamed' in i]  # remove unnamed columns from choices
        except:
            xvarchoices = ['No valid choices!']
        return xvarchoices

    def plot_spect_change_vars(self, obj):
        obj.clear()
        try:
            vars_level0 = self.data[self.chooseDataComboBox.currentText()].df.columns.get_level_values(0)
            vars_level1 = self.data[self.chooseDataComboBox.currentText()].df.columns.get_level_values(1)
            vars_level1 = vars_level1[vars_level0 == 'meta']

            try:
                vars_level1 = [i for i in vars_level1 if
                                    'Unnamed' not in str(i)]  # remove unnamed columns from choices
            except:
                pass
            choices = vars_level1

        except:
            try:
                choices = self.data[self.chooseDataComboBox.currentText()].columns.values
            except:
                choices = ['No valid choices']
        for i in choices:
            obj.addItem(str(i))

    def plot_spect_update_list(self, obj):
        try:
            obj.clear()
            self.data[self.chooseDataComboBox.currentText()]=spectral_data(enumerate_duplicates(
                self.data[self.chooseDataComboBox.currentText()].df,
                self.chooseColumnComboBox.currentText()))
            rowchoices = self.data[self.chooseDataComboBox.currentText()].df[
                ('meta', self.chooseColumnComboBox.currentText())]
            for i in rowchoices:
                obj.addItem(i)
        except:
            pass

    def set_spect_minmax(self,set_x=True, set_y=True):

        try:
            xvar = self.xVariableListWidget.selectedItems()[0].text()
            datatemp = self.data[self.chooseDataComboBox.currentText()].df

            if set_x:
                vars = datatemp[xvar].columns.values
                self.xminDoubleSpinBox.setValue(min(vars))
                self.xmaxDoubleSpinBox.setValue(max(vars))
            if set_y:
                ycol = self.chooseColumnComboBox.currentText()
                yrow = self.chooseRowsListWidget.selectedItems()[0].text()
                vals = datatemp[datatemp[('meta',ycol)] == yrow][xvar]
                self.yminSpinBox.setValue(vals.min(axis=1))
                self.ymaxSpinBox.setValue(vals.max(axis=1))
        except:
            pass

    def on_pushButton_clicked(self):
        filename, _filter = QtWidgets.QFileDialog.getSaveFileName(None, "Save Plot", self.outpath, "(*.png)")
        self.plotFilenameLineEdit.setText(filename)
        if self.plotFilenameLineEdit.text() == "":
            self.plotFilenameLineEdit.setText("*.png")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    Form = QtWidgets.QWidget()
    ui = PlotSpectra()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
