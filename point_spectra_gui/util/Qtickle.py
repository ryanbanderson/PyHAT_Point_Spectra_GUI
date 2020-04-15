import inspect
from distutils.util import strtobool

from PyQt5 import QtCore
from PyQt5.QtWidgets import *


class Qtickle(object):
    """
    A script designed to aid in saving values inside Qt objects.
    It works by inspecting for `objectnames` and then collecting their
    values.

    The name is a portmanteau of Qt and pickle. Originally the script
    utilized pickle to save data. Now data is returned in the form of
    a dictionary. This way the user gets to choose what happens to the
    data
    """

    def __init__(self, ui):
        self.ui = ui

    def guiSave(self):
        """
        Save all values in a particular UI

        :return:
        """
        dict = {}
        # Save geometry
        # self.settings.setValue('size', self.core.size())
        # self.settings.setValue('pos', self.core.pos())
        try:
            for name, obj in inspect.getmembers(self.ui):
                if isinstance(obj, QLineEdit):
                    name = obj.objectName()
                    value = obj.text()
                    dict[name] = value

                if isinstance(obj, QCheckBox):
                    name = obj.objectName()
                    state = obj.isChecked()
                    dict[name] = state

                if isinstance(obj, QRadioButton):
                    name = obj.objectName()
                    value = obj.isChecked()  # get stored value from registry
                    dict[name] = value

                if isinstance(obj, QSpinBox):
                    name = obj.objectName()
                    value = obj.value()  # get stored value from registry
                    dict[name] = value

                if isinstance(obj, QDoubleSpinBox):
                    name = obj.objectName()
                    value = obj.value()
                    dict[name] = value

                if isinstance(obj, QSlider):
                    name = obj.objectName()
                    value = obj.value()  # get stored value from registry
                    dict[name] = value

                if isinstance(obj, QLabel):
                    name = obj.objectName()
                    value = obj.text()
                    dict[name] = value

                if isinstance(obj, QComboBox):
                    values = []  # the list that will hold all values from QCombobox
                    name = obj.objectName()  # get the QCombobox object's name
                    for i in range(obj.count()):  # QCombobox contains a number of items
                        itemData = obj.itemText(i)
                        values.append(itemData)  # put those items into a list for saving
                    index = obj.findText(obj.currentText())  # return the index of the item, assign to selected
                    dict[name + "_values"] = values  # save all the values in settings
                    dict[name + "_index"] = index  # save the indexed value in settings

                if isinstance(obj, QListWidget):
                    values = []
                    name = obj.objectName()
                    for i in range(obj.count()):
                        itemData = obj.item(i).text()
                        values.append(itemData)
                    dict[name + "_values"] = values
                    # since there is a possibility of multiple items,
                    # we'll just save the string representation of those items to be restored
                    dict[name + "_index"] = [str(x.text()) for x in obj.selectedItems()]

            return dict
        except Exception as e:
            print(e)

    def guiRestore(self, dict):
        """
        Restore the GUI. This is a hard restore, meaning that everything will be overwritten

        :param dict:
        :return:
        """
        # Restore geometry
        # self.core.resize(self.settings.value('size', QtCore.QSize(500, 500)))
        # self.core.move(self.settings.value('pos', QtCore.QPoint(60, 60)))
        for name, obj in inspect.getmembers(self.ui):
            try:
                if isinstance(obj, QLineEdit):
                    name = obj.objectName()
                    value = dict[name]
                    obj.setText(value)  # restore lineEditFile

                if isinstance(obj, QCheckBox):
                    name = obj.objectName()
                    value = dict[name]
                    if value is not None:
                        try:
                            obj.setChecked(strtobool(value))  # restore checkbox
                        except:
                            obj.setChecked(value)

                if isinstance(obj, QRadioButton):
                    name = obj.objectName()
                    value = dict[name]
                    if value is not None:
                        obj.setChecked(strtobool(value))

                if isinstance(obj, QSlider):
                    name = obj.objectName()
                    value = dict[name]
                    if value is not None:
                        obj.setValue(int(value))  # restore value from registry

                if isinstance(obj, QSpinBox):
                    name = obj.objectName()
                    value = dict[name]
                    if value is not None:
                        obj.setValue(int(value))  # restore value from registry

                if isinstance(obj, QDoubleSpinBox):
                    name = obj.objectName()
                    value = dict[name]
                    if value is not None:
                        obj.setValue(float(value))

                if isinstance(obj, QLabel):
                    name = obj.objectName()
                    value = dict[name]
                    if value is not None:
                        obj.setText(value)

                if isinstance(obj, QComboBox):
                    name = obj.objectName()
                    values = dict[name + "_values"]
                    # clear all the objects
                    # so that we don't run into issues
                    # with restoring the list of values
                    obj.clear()
                    if values is not None:
                        for value in values:
                            if not (value == '' or value == "") and len(value) > 0:
                                # if there are some values in the list, we should add them to the Combobox
                                obj.addItem(value)

                    index = dict[name + "_index"]  # next we want to select the item in question by getting it's index
                    obj.setCurrentIndex(int(index))

                if isinstance(obj, QListWidget):
                    name = obj.objectName()
                    values = dict[name + "_values"]
                    index = dict[name + "_index"]
                    obj.clear()
                    if values is not None:
                        for value in values:
                            list_item = QListWidgetItem(value)
                            obj.addItem(list_item)
                        for i in index:
                            matching_items = obj.findItems(i, QtCore.Qt.MatchExactly)
                            for item in matching_items:
                               item.setSelected(True)

            except Exception as e:
                pass
                #print(e)

    def guiChanged(self, functionCall):
        """
        when the UI changes run the parameter `functionCall`

        :param functionCall:
        :return:
        """
        try:
            for name, obj in inspect.getmembers(self.ui):
                if isinstance(obj, QLineEdit):
                    obj.editingFinished.connect(lambda: functionCall())

                if isinstance(obj, QCheckBox):
                    obj.stateChanged.connect(lambda: functionCall())

                if isinstance(obj, QRadioButton):
                    obj.toggled.connect(lambda: functionCall())

                if isinstance(obj, QSpinBox):
                    obj.valueChanged.connect(lambda: functionCall())

                if isinstance(obj, QDoubleSpinBox):
                    obj.valueChanged.connect(lambda: functionCall())

                if isinstance(obj, QSlider):
                    obj.event.connect(lambda: functionCall())

                if isinstance(obj, QComboBox):
                    obj.currentIndexChanged.connect(lambda: functionCall())

                    # if isinstance(obj, QListWidget): This needs to be added at somepoint
                    #     obj.

        except Exception as e:
            print(e)

    def guiDisonnect(self):
        """
        This is mainly a problem with the buttons that were opening file dialogs, but if there are other cases,
        please consider adding those cases to this method.

        https://stackoverflow.com/questions/3530590/qt-signals-and-slot-connected-twice-what-happens#_=_
        Just like in this stackoverflow question, there are some instances where the UI will call connects
        more than once... this is dangerous as it causes dialog boxes to display also more than once.
        This method is an attempt to cull this problem.

        :return:
        """
        try:
            for name, obj in inspect.getmembers(self.ui):
                if isinstance(obj, QPushButton):
                    obj.disconnect()

        except Exception as e:
            print(e)

    def selectiveGuiRestore(self, dict):
        """
        Restore the GUI. This is a softer restore in regards to comboboxes.
        Comboboxes will not be overwritten but instead will be given an index to set themselves to.
        Everything else will continue to be overwritten, be careful.


        :param dict:
        :return:
        """
        for name, obj in inspect.getmembers(self.ui):
            pass
            try:
                if isinstance(obj, QCheckBox):
                    name = obj.objectName()
                    value = dict[name]
                    if value is not None:
                        try:
                            obj.setChecked(strtobool(value))  # restore checkbox
                        except:
                            obj.setChecked(value)

                if isinstance(obj, QRadioButton):
                    name = obj.objectName()
                    value = dict[name]
                    if value is not None:
                        obj.setChecked(strtobool(value))

                if isinstance(obj, QSlider):
                    name = obj.objectName()
                    value = dict[name]
                    if value is not None:
                        obj.setValue(int(value))  # restore value from registry

                if isinstance(obj, QSpinBox):
                    name = obj.objectName()
                    value = dict[name]
                    if value is not None:
                        obj.setValue(int(value))  # restore value from registry

                if isinstance(obj, QDoubleSpinBox):
                    name = obj.objectName()
                    value = dict[name]
                    if value is not None:
                        obj.setValue(float(value))

                if isinstance(obj, QComboBox):
                    name = obj.objectName()
                    # select the item in question by setting it's index
                    index = dict[name + "_index"]
                    obj.setCurrentIndex(int(index))

                if isinstance(obj, QListWidget):
                    name = obj.objectName()
                    index = dict[name + "_index"]
                    for i in index:
                        matching_items = obj.findItems(i, QtCore.Qt.MatchExactly)
                        for item in matching_items:
                            obj.setCurrentItem(item)
            except Exception as e:
                pass
                #print(e)
