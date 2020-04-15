import inspect
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import *
from point_spectra_gui.util import Qtickle


class Modules:
    """
    Modules class that UI modules will inherit from.

    *Note: Rigorous prototyping is still occurring
    So, naturally, assume that something in this class
    is always getting changed or added to better serve
    all cases in each UI class.

    ...

    Since `Modules` is shared among all the UI
    classes it would make sense that we would have
    some variables, that are necessary among all these
    classes, be put here in a high place where they
    can be referenced often.
    """
    data = {}  # initialize with an empty dict to hold data frames
    datakeys = []  # hold all the specific key for a specific data frame
    data_count = -1
    modelkeys = []
    models = {}  # For regression training
    model_count = -1
    predictkeys = []
    outpath = './'  # Default outpath; can be changed with OutputFolder.py
    figs = {}
    figname = []
    model_xvars = {}
    model_yvars = {}
    parent = []
    dimred = {} #for storing dimensionality reduction models
    dimredkeys = []


    def __init__(self):
        self.qtickle = Qtickle.Qtickle(self)
        self.settings = QSettings('USGS', 'PPSG')

    def setupUi(self, Form):
        self.Form = Form
        self.Form.mousePressEvent = self.mousePressEvent
        self.connectWidgets()

    def mousePressEvent(self, QMouseEvent):
        """
        TODO: Add right click event
        The hope is that we can add a right click dialogue for users
        The dialogue would give the option to delete particular
        modules from the UI, or insert modules, or copy modules.
        """
        # TODO Add mouse Event
        pass
        # print("Right Button Clicked {}".format(type(self).__name__))

    def get_widget(self):
        """
        This function specifies the variable that holds the
        styling. Use this function to get the variable

        :return:
        """
        raise NotImplementedError(
            'The method "get_widget()" was not found in the module {}'.format(type(self).__name__))

    def connectWidgets(self):
        """
        Connect the necessary widgets.

        :return:
        """
        raise NotImplementedError(
            'The method "connectWidgets()" was not found in the module {}'.format(type(self).__name__))

    def disconnectWidgets(self):
        """
        Disconnect the widgets that way we don't run into this problem
        https://stackoverflow.com/questions/3530590/qt-signals-and-slot-connected-twice-what-happens#_=_

        :return:
        """
        self.qtickle = Qtickle.Qtickle(self)
        self.qtickle.guiDisonnect()

    def getMainWindowParent(self):
        return self.parent[0]

    def guiChanged(self):
        self.qtickle = Qtickle.Qtickle(self)
        self.qtickle.guiChanged(self.getMainWindowParent().setupModules)

    def getGuiParams(self):
        """
        Return the contents from lineEdits, comboBoxes, etc.

        :return:
        """
        self.qtickle = Qtickle.Qtickle(self)
        s = self.qtickle.guiSave()
        return s

    def setGuiParams(self, dict):
        """
        Using a dictionary, restore the UI

        :param dict:
        :return:
        """
        self.qtickle = Qtickle.Qtickle(self)
        self.qtickle.guiRestore(dict)

    def selectiveSetGuiParams(self, dict):
        """
        Selectively restore the UI.
        We don't want to lose the content we have selected
        but we don't want to override crucial information either

        :param dict:
        :return:
        """
        self.qtickle = Qtickle.Qtickle(self)
        self.qtickle.selectiveGuiRestore(dict)

    def setup(self):
        """
        This is a stripped down version of run()
        Each Module's functionality will be quickly ran through, so we have
        at least something in the UI to work with

        :return:
        """
        pass

    def run(self):
        """
        Each Module's functionality will be ran in this function.
        You will define what will happen to the data and parameters in here
        :return:
        """
        raise NotImplementedError('The method "run()" was not found in the module {}'.format(type(self).__name__))

    def delete(self):
        """
        In some particular cases, the UI needs to have some information dumped.
        This is a chance to do that.

        :return:
        """
        pass

    def isEnabled(self):
        """
        Checks to see if current widget isEnabled or not
        :return:
        """
        return self.get_widget().isEnabled()

    def setDisabled(self, bool):
        """
        After every execution we want to prevent the user from changing something.
        So, disable the layout by greying it out

        :param bool:
        :return:
        """
        self.get_widget().setDisabled(bool)

    def setProgressBar(self, progressBar):
        """
        This function makes it possible to reference the progress bar
        in MainWindow

        :param progressBar:
        :return:
        """
        self.progressBar = progressBar

    def checkMinAndMax(self):
        """
        Go through the entire UI and set the maximums and minimums of each widget

        :return:
        """
        for name, obj in inspect.getmembers(self):
            if isinstance(obj, QSpinBox):
                obj.setMaximum(999999)

            if isinstance(obj, QDoubleSpinBox):
                obj.setDecimals(7)

    @staticmethod
    def getChangedValues(input_dictionary, algorithm):
        """
        Check symmetrically if the values in the dictionary match with values in the algorithm
        If they don't, then we will want to record those changed values.

        Example input: getChangedValues(methodParameters, AirPLS())

        :param input_dictionary:
        :param algorithm:
        :return:
        """
        dic = {}
        for key in input_dictionary:
            if input_dictionary[key] != getattr(algorithm, key):  # key gives us a string
                dic.update({key: input_dictionary[key]})
        return dic

    @staticmethod
    def setComboBox(comboBox, keyValues):
        """
        Sets up the information inside comboBox widgets
        This function does not need to be overridden.

        :param comboBox: QtWidgets.QComboBox
        :param keyValues: []
        :return:
        """
        comboBox.clear()
        comboBox.setMaximumWidth(400)
        try:
            keyValues = [str(i) for i in keyValues] #force all elements of the list to be strings
        except:
            pass
        comboBox.addItems(keyValues)


    @staticmethod
    def changeComboListVars(obj, newchoices):
        """
        Function changes combo boxes or list widgets
        This function does not need to be overridden.

        :param obj:
        :param newchoices:
        :return:
        """
        if isinstance(obj, QComboBox):
            obj_sel = obj.currentIndex()
        elif isinstance(obj, QListWidget):
            obj_sel = [x for x in obj.selectedIndexes()]
        obj.clear()
        for i in newchoices:
            if isinstance(i, tuple):
                obj.addItem(str(i[1]))
            elif isinstance(i, str):
                obj.addItem(i)
        if isinstance(obj,QComboBox):
            obj.setCurrentIndex(obj_sel)
        elif isinstance(obj, QListWidget):
            for indx in obj_sel:
                obj.setCurrentItem(obj.itemFromIndex(indx))
    @staticmethod
    def setListWidget(obj, choices):
        """
        Function changes lists
        This function does not need to be overridden

        :param obj:
        :param choices:
        :return:
        """

        # obj_sel = [x for x in obj.selectedIndexes()] #save the currently selected items
        obj.clear() #clear the list

        for item in choices: #repopulate the list with the new choices
            obj.addItem(item)
        # for indx in obj_sel: #re-select the items
        #     obj.setCurrentItem(obj.itemFromIndex(indx))


    @staticmethod
    def defaultComboItem(obj, item):
        """
        Set the default selected item in a box.

        :param obj:
        :param item:
        :return:
        """
        obj.setCurrentIndex(obj.findText(str(item)))

    @staticmethod
    def list_amend(list_, count_, input_):
        """
        In some cases a list is never actually instantiated.
        To fix this, we want to first try and see if we can access a particular count
        If that doesn't work due to an IndexError then we'll just settle for appending

        :param list_:
        :param count_:
        :param input_:
        :return:
        """
        try:
            list_[count_] = input_
        except IndexError:
            list_.append(input_)
