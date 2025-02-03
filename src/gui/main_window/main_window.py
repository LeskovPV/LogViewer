# coding=utf-8

import os
from PySide6.QtWidgets import QMainWindow

from utils.plot_generator import PlotGenerator, PlotData
from utils.ui2widget import Ui2WidgetLoader


class MainWindow(QMainWindow):
    """
    Главное окно
    """

    def __init__(self):
        super().__init__()
        Ui2WidgetLoader().loadUi2Widget(f'{os.path.splitext(__file__)[0]}.ui', self)  # Загрузка ui в self

        plot_data = PlotData()
        plot_data.add_y_data(y_data=[10,0], title='Ещё график', by_right_scale=True)
        # axes_id=plot_data.add_axes(x_data=[1,4,5,8,9], axes_title='Вторые координаты:')
        # plot_data.add_y_data(axes_id=axes_id, y_data=[4,5,1,10,0], y_title='Ещё график', by_right_scale=True)
        PlotGenerator(plot_widget=self.tab_3).set_plot(plot_data=plot_data)
        # pg.set_plot()

    # def initialize_ui(self):
    #     LogViewer().view(**dict(zip(['this_file', 'cfg_file', 'log_file'], sys.argv)))
    #
    #     # plot_widget = LogViewer().get_plot_widget(**dict(zip(['this_file', 'cfg_file', 'log_file'], sys.argv)))

