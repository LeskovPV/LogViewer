# coding=utf-8

import os
from PySide6.QtWidgets import QMainWindow
from matplotlib.pyplot import title

from utils.plot_widget import CanvasData, PlotData, AxesData, PlotWidget
from utils.ui2widget import Ui2WidgetLoader


class MainWindow(QMainWindow):
    """
    Главное окно
    """

    def __init__(self):
        super().__init__()
        Ui2WidgetLoader().loadUi2Widget(f'{os.path.splitext(__file__)[0]}.ui', self)  # Загрузка ui в self

        canvas_data = CanvasData(
            title='Проверочный график',
            axeses=[
                AxesData(
                    x_data=[0, 1, 2, 3],
                    plots=[
                        PlotData(
                            y_data=[0, 1, 7, 4]),
                        PlotData(
                            y_data=[10, 21, 17, 14],
                            by_right_scale=True)]),
                AxesData(
                    x_data=[1, 2, 3],
                    plots=[
                        PlotData(
                            y_data=[30, 21, 17],
                            by_right_scale=True)])
            ])

        PlotWidget(parent=self.tab_3, canvas_data=canvas_data)

    # def initialize_ui(self):
    #     LogViewer().view(**dict(zip(['this_file', 'cfg_file', 'log_file'], sys.argv)))
    #
    #     # plot_widget = LogViewer().get_plot_widget(**dict(zip(['this_file', 'cfg_file', 'log_file'], sys.argv)))

