# coding=utf-8

import asyncio
import os
from PySide6.QtWidgets import QMainWindow, QProgressBar, QLabel

from utils.plot_widget import CanvasData, PlotData, AxesData, PlotWidget
from utils.ui2widget import Ui2WidgetLoader


class MainWindow(QMainWindow):
    """
    Главное окно
    """
    COUNT = 1e3
    index = 0

    @classmethod
    async def test_calc(cls, progress_bar: QProgressBar = None, label: QLabel = None):
        print('Поехали')
        if progress_bar is not None:
            progress_bar.setMaximum(cls.COUNT)
        try:
            while True:
                cls.index += 1
                print(f'index = {cls.index}')
                if label is not None:
                    label.setText(f'index = {cls.index}')
                if progress_bar is not None:
                    progress_bar.setValue(cls.index)
                await asyncio.sleep(0.01)
                if cls.index > cls.COUNT:
                    break
        except asyncio.CancelledError:
            print('Стоямба')
        result = cls.index
        cls.index = 0
        if label is not None:
            label.setText(f'index = 0')
        if progress_bar is not None:
            progress_bar.setValue(0)
        return result

    def on_stop_task(self, task):
        message = f'Task is finished with result "{task.get_name()}": {task._result}'
        print(message)
        self._task = None

    def on_button_clicked(self):
        if self._task is None:
            self._task = asyncio.create_task(self.test_calc(self.progressBar, self.label), name='Test calc')
            self._task.add_done_callback(self.on_stop_task)
        else:
            self._task.cancel()

    def __init__(self):
        super().__init__()
        self._task = None
        Ui2WidgetLoader().loadUi2Widget(f'{os.path.splitext(__file__)[0]}.ui', self)  # Загрузка ui в self
        self.button.clicked.connect(self.on_button_clicked)
        self.label.setText(f'index = {0}')
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

