# coding=utf-8

from datetime import datetime
from os import path

from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates
from matplotlib import colors
from resourses.dirs import CFG_FILE, LOG_FILE
from tools.structures import Device, Record


class LogViewer:
    """Загрузчик журнала"""

    def view(self,
             cfg_file: str = CFG_FILE,
             log_file: str = LOG_FILE,
             **kwargs):
        """
        Загрузка журнала [и отображение его графике]
        :param cfg_file: Конфиг-файл с описанием устройств
        :param log_file: Лог-файл, содержащий записи журнала
        :return:
        """

        devices = list()  # Полный список устройств (из cfg-файла)
        ammeters_ranges = dict()  # Диапазоны измерений амперметров
        voltmeter_range = tuple()  # Диапазоны измерений вольтметра

        try:
            with open(cfg_file, 'r') as file:  # Читаем список устройств из cfg-файла
                while line := file.readline():
                    device = Device(*line[:-1].split('\t'))
                    devices.append(device)
                    if device.unit == 'А':
                        ammeters_ranges[device.ip_addr] = (float(device.range_start), float(device.range_stop))
                    else:
                        voltmeter_range = (float(device.range_start), float(device.range_stop))
        except Exception as exception:
            print(exception)
            return

        power = dict()  # Результирующий справочник со значениями мощности (ключ - время, значение - мощность)
        voltage = dict()  # Результирующий справочник со значениями напряжения (ключ - время, значение - напряжение)
        amperage = dict()  # Результирующий справочник со значениями силы тока (ключ - время, значение - сила тока)
        ammeter_amperage = dict()  # Cправочник амперметров (ключ - адрес устройства, значение - справочник со значениями силы тока (см.выше) )
        voltage_value = None  # Изначально, вольтаж неизвестем
        try:
            with open(log_file, 'r') as file:  # Читаем журнал из log-файла
                while line := file.readline():
                    record = Record(*line[:-1].split('\t'))
                    record.value = float(record.value)
                    record.moment = datetime.strptime(record.moment, '%Y.%m.%d %H:%M:%S.%f')
                    if record.ip_addr in ammeters_ranges:  # читаем ампераж, если адрес амперметра
                        if voltage_value is None:  # Если вольтаж еще не определён
                            continue  # переходим к следующей записи журнала
                        ammeter_range_start, ammeter_range_stop = ammeters_ranges[record.ip_addr]
                        if ammeter_range_start <= record.value <= ammeter_range_stop:  # Если значение попадает в изм.диапазон
                            amperage[record.moment] = record.value
                            power[record.moment] = voltage_value * record.value
                        else:
                            pass  # Пропускаем запись амперметра, когда его значение лежит вне диапазона
                        if record.ip_addr not in ammeter_amperage.keys():
                            ammeter_amperage[record.ip_addr] = dict()
                        ammeter_amperage[record.ip_addr][record.moment] = record.value
                    else:  # иначе, читаем вольтаж
                        if voltage_value is None:  # Если вольтаж еще не определён
                            plot_title = record.moment.strftime('%d.%m.%Y')
                            voltage_addr = record.ip_addr
                        voltage_value = record.value
                        voltage[record.moment] = voltage_value
        except Exception as exception:
            print(exception)
            return


        plt.figure().canvas.manager.set_window_title('Обозреватель журнала')  # Заголовок окна
        plt.suptitle('Измерения от {}'.format(plot_title), fontweight='bold')  # Название графика

        plt.subplot(3, 1, 1)  # указываем 2 строки, 1 столбец, выбираем первое место
        plt.title('Журнал: {}\nКонфигурация: {}\n'.format(log_file, cfg_file))  # Название графика
        plt.ylabel('Сила тока, А')  # Подпись для оси y
        _h, _s, _v = colors.rgb_to_hsv(colors.hex2color('#9FFEA5'))
        for ip_addr, _amperage in ammeter_amperage.items():
            _h += 1.0 / len(ammeter_amperage)
            if _h > 1.0:
                _h = _h - 1.0
            _clr = colors.hsv_to_rgb([_h, _s, _v])
            _label = '{}:  {} - {}А'.format(ip_addr, *ammeters_ranges[ip_addr])
            plt.plot_date(_amperage.keys(), _amperage.values(), linestyle='solid', color=_clr, label=_label)
        plt.plot_date(amperage.keys(), amperage.values(), color='black', label='Выборка')
        plt.legend(loc='best')  # Устанавливаем легенду в оптимальное место

        plt.subplot(3, 1, 2)  # указываем 2 строки, 1 столбец, выбираем первое место
        plt.ylabel('Напряжение, В')  # Подпись для оси y
        _label = '{}:  {} - {}В'.format(voltage_addr, *voltmeter_range)
        plt.plot_date(voltage.keys(), voltage.values(), linestyle = 'solid', color='black', label=_label)
        plt.legend(loc='best')  # Устанавливаем легенду в оптимальное место

        plt.subplot(3, 1, 3)  # указываем 2 строки, 1 столбец, выбираем первое место
        plt.ylabel('Мощность, Вт')  # Подпись для оси y
        plt.plot_date(power.keys(), power.values(), linestyle = 'solid', color='black')

        plt.gca().xaxis.set_major_formatter(mpl_dates.DateFormatter('%H:%M:%S'))
        plt.show()