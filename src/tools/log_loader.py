# coding=utf-8
from datetime import datetime

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import dates as mpl_dates
from resourses.dirs import CFG_FILE, LOG_FILE
from tools.structures import Device, Record


class LogLoader:
    """Загрузчик журнала"""

    def load(self,
             cfg_file: str = CFG_FILE,
             log_file: str = LOG_FILE):

        devices = list()  # Полный список устройств (из cfg-файла)
        ammeters_ranges = dict()  # Диапазоны измерений амперметров

        with open(cfg_file, 'r') as file:  # Читаем список устройств из cfg-файла
            while line := file.readline():
                device = Device(*line[:-1].split('\t'))
                devices.append(device)
                if device.unit == 'А':
                    ammeters_ranges[device.ip_addr] = (float(device.range_start), float(device.range_stop))

        power = dict()  # Результирующий справочник со значениями мощности (ключ - время, значение - мощность)
        voltage = None  # Изначально, вольтаж неизвестем
        with open(log_file, 'r') as file:  # Читаем журнал из log-файла
            while line := file.readline():
                record = Record(*line[:-1].split('\t'))
                record.value = float(record.value)
                record.moment = datetime.strptime(record.moment, '%Y.%m.%d %H:%M:%S.%f')
                if record.ip_addr in ammeters_ranges:  # читаем ампераж, если адрес амперметра
                    if voltage is None:  # Если вольтаж еще не определён
                        continue  # переходим к следующей записи журнала
                    ammeter_range_start, ammeter_range_stop = ammeters_ranges[record.ip_addr]
                    if ammeter_range_start <= record.value <= ammeter_range_stop:  # Если значение попадает в изм.диапазон
                        power[record.moment] = voltage * record.value
                    else:
                        pass  # Пропускаем запись амперметра, когда его значение лежит вне диапазона
                else:  # иначе, читаем вольтаж
                    voltage = record.value
                    plot_title = record.moment.strftime('%d.%m.%Y')

        plt.figure().canvas.manager.set_window_title('Обозреватель журнала')  # Заголовок окна
        plt.title('Измерения от ' + plot_title, fontweight='bold')  # Название графика
        plt.xlabel('Время')  # Подпись для оси х
        plt.ylabel('Мощность, Вт')  # Подпись для оси y
        plt.plot_date(power.keys(), power.values(), linestyle = 'solid')
        plt.gca().xaxis.set_major_formatter(mpl_dates.DateFormatter('%H:%M:%S'))
        plt.show()