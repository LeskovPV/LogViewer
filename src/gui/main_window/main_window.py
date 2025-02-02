# coding=utf-8

import os
from PySide6.QtWidgets import QMainWindow

from utils.plot_generator import PlotGenerator
from utils.ui2widget import Ui2WidgetLoader


class MainWindow(QMainWindow):
    """
    Главное окно
    """

    def __init__(self):
        super().__init__()
        Ui2WidgetLoader().loadUi2Widget(f'{os.path.splitext(__file__)[0]}.ui', self)  # Загрузка ui в self

        PlotGenerator(plot_widget=self.tab_3, plot_title='tab_3').set_plot()
        pg = PlotGenerator(plot_widget=self.tab)
        self.button.clicked.connect(lambda: pg.set_plot())
        # pg.set_plot()

    # def initialize_ui(self):
    #     LogViewer().view(**dict(zip(['this_file', 'cfg_file', 'log_file'], sys.argv)))
    #
    #     # plot_widget = LogViewer().get_plot_widget(**dict(zip(['this_file', 'cfg_file', 'log_file'], sys.argv)))

