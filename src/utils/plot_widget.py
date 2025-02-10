from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

import matplotlib
from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.ticker import AutoMinorLocator

from utils.attr_dict import AttrDict

matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure

@dataclass
class PlotData:
    y_data: list[int | float] = field(default_factory=list)
    title: str = 'График'
    by_right_scale: bool = False
    line_type: int = 0

@dataclass
class AxesData:
    x_data: list[int | float | datetime] = field(default_factory=list)
    plots: list[PlotData] = field(default_factory=list)
    title: str = None
    x_label: str = 'Ось X'
    y_label: str = 'Ось Y'
    y_right_label: str = 'Ось Y справа'

@dataclass
class CanvasData:
    axeses: list[AxesData] = field(default_factory=list)
    title: str = 'Заголовок'


class PlotWidget(QWidget):
    """
    Виджет для отрисовки графиков
    """

    FONTS_SIZES = AttrDict(  # Размеры шрифтов:
        suptitle = 18,  # для общего заголовка
        axes_title = 14,  # для надписи систем координат
        axes_label = 14,  # для меток координатных осей
    )

    def __init__(self,
                 parent: QWidget = None,
                 canvas_data: CanvasData = None,
                 dpi: int = 100):
        super().__init__(parent=parent)
        self.figure = Figure(figsize=(parent.size().width(), parent.size().height()), dpi=dpi)
        if isinstance(parent, QWidget):
            (QVBoxLayout(parent) if parent.layout() is None else parent.layout()).addWidget(self)
        self.redraw(canvas_data=canvas_data)


    def redraw(self, canvas_data: CanvasData):
        if canvas_data is None:
            return

        self.figure.clear()

        if canvas_data.title is not None:
            self.figure.suptitle(canvas_data.title, fontweight='bold', fontsize = self.FONTS_SIZES.suptitle)

        for axes in canvas_data.axeses:
            self.axes = self.figure.add_subplot(len(canvas_data.axeses), 1, canvas_data.axeses.index(axes) + 1)

            #if axes_title is not None:
            self.axes.set_title(axes.title, fontsize=self.FONTS_SIZES.axes_title)  # Надпись системы координат
            self.axes.grid(which="major", linewidth=1.2)
            self.axes.grid(which="minor", linestyle="--", color="gray", linewidth=0.5)

            # import numpy as np
            # x = np.linspace(0, 10, 10)
            self.axes.set_xlabel(axes.x_label, fontsize=self.FONTS_SIZES.axes_label)
            twinx_axes = None
            for plot in axes.plots:
                if plot.by_right_scale and twinx_axes is None:
                    twinx_axes = self.axes.twinx()
                current_axes = twinx_axes if plot.by_right_scale else self.axes
                # title = plot_data.axeses[axes_id].y_right_title if plot.by_right_scale else plot_data.axeses[axes_id].y_title
                # current_axes.scatter(axes.x_data, plot.y_data, label=plot.title, color='red')
                current_axes.plot(axes.x_data, plot.y_data, label=plot.title)
                current_axes.set_ylabel(axes.y_right_label if plot.by_right_scale else axes.y_label, fontsize=self.FONTS_SIZES.axes_label)

            # self.axes.plot(x, y2, label="y2 = x^2")
            # self.axes.legend()
            # self.axes.scatter(x, y1, c="red", label="y1 = 4*x")
            # self.axes.plot(x, y2, label="y2 = x^2")

            self.axes.legend()  # Вывод легенды
            self.axes.xaxis.set_minor_locator(AutoMinorLocator())  # Минорные насечки на оси X
            self.axes.yaxis.set_minor_locator(AutoMinorLocator())  # Минорные насечки на оси Y
            # self.axes.tick_params(which='major', length=10, width=2)  # Мажорные насечки на оси
            # self.axes.tick_params(which='minor', length=5, width=1)  # Минорные насечки на оси

        _figure_canvas = FigureCanvasQTAgg(self.figure)
        if self.layout() is None:
            self.plot_layout = QVBoxLayout(self)
            self.plot_layout.addWidget(NavigationToolbar2QT(_figure_canvas, self))
        else:
            self.plot_layout = self.layout()
        # for c in self.plot_widget.children():
        #     if isinstance(c, FigureCanvasQTAgg):
        #         self.plot_widget.
        self.plot_layout.addWidget(_figure_canvas)
