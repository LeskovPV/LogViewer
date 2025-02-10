# coding=utf-8
import json

from gui.main_window.main_window import MainWindow
from utils.plot_widget import AxesData, PlotData, CanvasData


def launch_ui(widget_class, **kwargs):
    """
    Запуск Q-приложения с экземпляром widget_class в качестве главного окна
    """
    import sys
    from PySide6.QtWidgets import QApplication
    # from PySide6.QtCore import Qt, QCoreApplication
    #
    # QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)  # расшарка ресурсов между контекстами OpenGL
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)  # Создание объекта приложения Qt

    widget = widget_class(**kwargs)
    widget.show()
    sys.exit(app.exec())  # Запуск приложения


if __name__ == "__main__":
    launch_ui(widget_class=MainWindow)
