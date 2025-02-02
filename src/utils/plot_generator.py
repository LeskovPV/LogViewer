from datetime import datetime

import matplotlib
from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.ticker import AutoMinorLocator
from numpy.ma.core import count

from utils.attr_dict import AttrDict

matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure

class PlotData:

    def __init__(self,
                 x_data: list[int|float|datetime],
                 y_data: list[int|float] = None,
                 plot_title: str = None,
                 x_title: str = None,
                 y_title: str = None,
                 y_label: str = None):
        self.plot_title = plot_title
        self.y_title = y_title
        self.axes = []
        self.add_axes(x_data=x_data, x_title=x_title)
        self.add_y_data(y_data=y_data, y_label=y_label)


    def add_axes(self,
                 x_data: list[int|float|datetime],
                 x_title: str = None,
                 y_title: str = None,
                 right_y_title: str = None):
        self.axes.append(AttrDict(
            x_data=x_data,
            x_title=x_title,
            y_title=y_title,
            right_y_title=right_y_title,
            y_datas=[]
        ))

    def add_y_data(self,
                   axes_id: int = 0,
                   y_data: list[int | float] = None,
                   y_label: str = None,
                   right_scale: bool = False,
                   line_type: int = 0):
        if axes_id not in range(len(self.axes)):
            return
        if len(y_data) != len(self.axes[axes_id].x_data):
            return
        self.axes[axes_id].y_datas.append(AttrDict(
            y_data=y_data,
            y_label=y_label,
            right_scale=right_scale,
            line_type=line_type
        ))




class PlotGenerator:
    """
    Генератор графиков
    """

    FONTS_SIZES = AttrDict(  # Размеры шрифтов:
        suptitle = 18,  # для общего заголовка
        axes_title = 14,  # для надписи систем координат
        axes_label = 14,  # для меток координатных осей
    )

    def __init__(self,
                 plot_widget: QWidget = None,
                 dpi: int = 100):
        self.plot_widget = plot_widget
        self.figure = Figure(figsize=(self.plot_widget.size().width(), self.plot_widget.size().height()), dpi=dpi)

    def set_plot(self,
                 plot_data: PlotData(
                     x_data=[0,1],
                     y_data=[0,1],
                     plot_title=None,
                     x_title='x',
                     y_title='y',
                     y_label='График №1')
                 ):
        self.figure.clear()
        if plot_title is not None:
            self.figure.suptitle(plot_title, fontweight='bold', fontsize = self.FONTS_SIZES.suptitle)

        self.axes = self.figure.add_subplot(2, 1, 2)
        #if axes_title is not None:
        self.axes.set_title(axes_title, fontsize=self.FONTS_SIZES.axes_title)  # Надпись системы координат
        self.axes.grid(which="major", linewidth=1.2)
        self.axes.grid(which="minor", linestyle="--", color="gray", linewidth=0.5)

        # import numpy as np
        # x = np.linspace(0, 10, 10)
        self.axes.set_xlabel(x_data[0], fontsize=self.FONTS_SIZES.axes_label)
        for y_data in y_datas:
            self.axes.set_ylabel('y_data[0]', fontsize=14)
            # self.axes.scatter(x_data[1], y_data[1], c="red", label=y_data[0])
            self.axes.plot(x_data[1], y_data[1], label=y_data[0])
        # self.axes.plot(x, y2, label="y2 = x^2")
        # self.axes.legend()
        # self.axes.scatter(x, y1, c="red", label="y1 = 4*x")
        # self.axes.plot(x, y2, label="y2 = x^2")

        self.axes.legend()  # Вывод легенды
        self.axes.xaxis.set_minor_locator(AutoMinorLocator())  # Минорные насечки на оси X
        self.axes.yaxis.set_minor_locator(AutoMinorLocator())  # Минорные насечки на оси Y
        # self.axes.tick_params(which='major', length=10, width=2)  # Мажорные насечки на оси
        # self.axes.tick_params(which='minor', length=5, width=1)  # Минорные насечки на оси

        sc = FigureCanvasQTAgg(self.figure)
        if self.plot_widget.layout() is None:
            self.plot_layout = QVBoxLayout(self.plot_widget)
            self.plot_layout.addWidget(NavigationToolbar2QT(sc, self.plot_widget))
        else:
            self.plot_layout = self.plot_widget.layout()
        # for c in self.plot_widget.children():
        #     if isinstance(c, FigureCanvasQTAgg):
        #         self.plot_widget.
        self.plot_layout.addWidget(sc)
