from datetime import datetime

import matplotlib
from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.ticker import AutoMinorLocator

from utils.attr_dict import AttrDict

matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure


class PlotData(AttrDict):

    def __init__(self,
                 plot_title: str = 'Заголовок',
                 x_data: list[int | float | datetime] = [0, 1],
                 y_data: list[int | float] = [0, 1],
                 x_label: str = 'Ось X',
                 y_label: str = 'Ось Y',
                 y_title: str = 'График'):
        super().__init__()
        self.plot_title = plot_title
        self.axeses = []
        self.add_axes(x_data=x_data, x_label=x_label, y_label=y_label)
        self.add_y_data(y_data=y_data, title=y_title)


    def add_axes(self,
                 x_data: list[int|float|datetime] = None,
                 axes_title: str = None,
                 x_label: str = 'Ось X',
                 y_label: str = 'Ось Y слева',
                 y_right_label: str = 'Ось Y справа'):
        if (x_data is None) and self.axeses_count > 0:
            x_data = self.axeses[self.axeses_count - 1].x_data
        self.axeses.append(AttrDict(
            axes_title=axes_title,
            x_data=x_data,
            x_label=x_label,
            y_label=y_label,
            y_right_label=y_right_label,
            y_datas=[]
        ))
        return self.axeses_count - 1

    def add_y_data(self,
                   axes_id: int = 0,
                   y_data: list[int | float] = [0, 1],
                   title: str = 'График',
                   by_right_scale: bool = False,
                   line_type: int = 0):
        if axes_id not in range(self.axeses_count):
            return
        if len(y_data) != len(self.axeses[axes_id].x_data):
            return
        self.axeses[axes_id].y_datas.append(AttrDict(
            y_data=y_data,
            title=title,
            by_right_scale=by_right_scale,
            line_type=line_type
        ))

    @property
    def axeses_count(self):
        return len(self.axeses)
p

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

    def set_plot(self, plot_data: PlotData):
        print(plot_data.get_json_format())
        self.figure.clear()

        if plot_data.plot_title is not None:
            self.figure.suptitle(plot_data.plot_title, fontweight='bold', fontsize = self.FONTS_SIZES.suptitle)

        for axes_id in range(plot_data.axeses_count):
            self.axes = self.figure.add_subplot(plot_data.axeses_count, 1, axes_id + 1)

            #if axes_title is not None:
            self.axes.set_title(plot_data.axeses[axes_id].axes_title, fontsize=self.FONTS_SIZES.axes_title)  # Надпись системы координат
            self.axes.grid(which="major", linewidth=1.2)
            self.axes.grid(which="minor", linestyle="--", color="gray", linewidth=0.5)

            # import numpy as np
            # x = np.linspace(0, 10, 10)
            self.axes.set_xlabel(plot_data.axeses[axes_id].x_label, fontsize=self.FONTS_SIZES.axes_label)
            self.axes.set_ylabel(plot_data.axeses[axes_id].y_label, fontsize=self.FONTS_SIZES.axes_label)
            twinx_axes = None
            for y_data in plot_data.axeses[axes_id].y_datas:
                if y_data.by_right_scale and twinx_axes is None:
                    twinx_axes = self.axes.twinx()
                current_axes = twinx_axes if y_data.by_right_scale else self.axes
                # title = plot_data.axeses[axes_id].y_right_title if y_data.by_right_scale else plot_data.axeses[axes_id].y_title
                title = y_data.title
                # self.axes.scatter(x_data[1], y_data[1], c="red", label=y_data[0])
                print(title)
                current_axes.plot(plot_data.axeses[axes_id].x_data, y_data.y_data, label=title)
            if twinx_axes is not None:
                twinx_axes.set_ylabel(plot_data.axeses[axes_id].y_right_label, fontsize=self.FONTS_SIZES.axes_label)
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
