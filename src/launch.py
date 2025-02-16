# coding=utf-8
import asyncio
import json
import sys

from PySide6 import QtAsyncio
from pyparsing import with_class
from sqlalchemy.util import await_only

from gui.main_window.main_window import MainWindow
from utils.attr_dict import AttrDict
from utils.plot_widget import AxesData, PlotData, CanvasData




def launch_ui(widget_class, **kwargs):
    """
    Запуск Q-приложения с экземпляром widget_class в качестве главного окна
    """
    from PySide6.QtWidgets import QApplication
    # from PySide6.QtCore import Qt, QCoreApplication
    #
    # QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)  # расшарка ресурсов между контекстами OpenGL
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)  # Создание объекта приложения Qt

    widget = widget_class(**kwargs)
    widget.show()
    #    sys.exit(app.exec())  # Запуск приложения в обычном режиме
    QtAsyncio.run(handle_sigint=True)  # Запуск приложения в режиме поддержки asyncio


if __name__ == "__main__":
    #print(sys.argv)
    _argv = AttrDict(**dict(zip(['this_file', 'cfg_file'], sys.argv)))
    if _argv.cfg_file is None:
        launch_ui(widget_class=MainWindow)
    else:
        result = asyncio.run(MainWindow.test_calc())
        message = f'Task is finished with result: {result}'
        print(message)
    # asyncio.run(async_launch_ui(widget_class=MainWindow))
