# coding=utf-8

from PySide6.QtCore import QMetaObject
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget


class Ui2WidgetLoader(QUiLoader):
    """
    Загрузчик интерфейса в виджет
    """

    host_widget = None

    def createWidget(self, classname, parent=None, name=''):
        """
        Переопределение метода
        """
        if parent is None and self.host_widget is not None:
            widget = self.host_widget
        else:
            widget = super().createWidget(classname, parent, name)
            if self.host_widget is not None:
                setattr(self.host_widget, name, widget)
        return widget


    def loadUi2Widget(self, ui_file: str, host_widget: QWidget):
        """
        Загрузка интерфейса в виджет
        :param ui_file: Файл интерфейса (*.ui), созданный в Qt Designer
        :param host_widget: Виджет, в который загружается ui (принимающий виджет)
        """
        self.host_widget = host_widget
        self.load(ui_file)
        QMetaObject.connectSlotsByName(host_widget)
