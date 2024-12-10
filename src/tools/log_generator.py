# coding=utf-8

import math
from random import random, randint
from datetime import datetime, timedelta
from resourses.dirs import CFG_FILE, LOG_FILE
from tools.structures import GenDevice


class LogGenerator:
    """Генератор тестовых данных"""


    def generate(self,
                 cfg_file: str = CFG_FILE,
                 log_file: str = LOG_FILE,
                 ammeters_ranges: list[tuple[float]] = [(0.0, 0.5), (0.2, 1.0), (1.0, 5.0), (3.0, 10.0)],
                 measurements_duration: int = 60,
                 time_step: int = 1):
        """
        Сгенерировать тестовые данные
        :param cfg_file: Конфиг-файл с описанием устройств
        :param log_file: Лог-файл, содержащий записи журнала
        :param ammeters_ranges: Диапазоны измерений амперметров
        :param measurements_duration: Продолжительность измерений, сек
        :param time_step: Примерный шаг по времени между измерениями, сек
        """
        self.start_time = datetime.now()  # Время начала измерений
        self.stop_time = self.start_time + timedelta(seconds=measurements_duration)  # Время окончания измерений
        self.measurements_duration = measurements_duration  # Продолжительность измерений, сек

        devices = []  # Список устройств
        addr_prefix = '10.0.0.'  # Адресный префикс
        device_number = 1  # Номер устройства и одновременно  адресный суфикс
        device_start_time = self.start_time
        device_time_step = timedelta(milliseconds=randint(int(0.9 * time_step * 1E3), int(1.1 * time_step * 1E3)))
        devices.append(GenDevice(
            ip_addr=f'{addr_prefix}{device_number}',
            range_start=0.0,
            range_stop=110.0,
            unit='В',
            start_time = device_start_time,
            time_step = device_time_step
        ))

        for ammeter_range in ammeters_ranges:
            device_number += 1
            device_start_time += timedelta(milliseconds=randint(0, int(time_step * 1E3)))
            device_time_step = timedelta(milliseconds=randint(int(0.9 * time_step * 1E3), int(1.1 * time_step * 1E3)))
            devices.append(GenDevice(
                ip_addr=f'{addr_prefix}{device_number}',
                range_start=ammeter_range[0],
                range_stop=ammeter_range[1],
                unit='А',
                start_time = device_start_time,
                time_step = device_time_step
            ))

        try:
            with open(cfg_file, 'w') as file:  # Записываем список устройств в конфиг-файл
                for device in devices:
                    file.write(f'{device.ip_addr}\t{device.range_start}\t{device.range_stop}\t{device.unit}\n')
        except Exception as exception:
            print(exception)

        journal = dict()  # Журнал {time: (ip_addr, value)}
        for device in devices: # Последовательно (для каждого устройства) генерируем значения и пишем в журнал
            measurement_time = device.start_time  # Первая запись в момент старта устройства
            while measurement_time < self.stop_time:
                journal[measurement_time] = (device.ip_addr, self._gen_value(device, measurement_time))
                measurement_time = measurement_time + device.time_step  # Вычисляем момент след.измерения
        try:
            with open(log_file, 'w') as file:  # Записываем список устройств в конфиг-файл
                for key, value in sorted(journal.items()):  # Сортируем журнал по ключу (т.е. по времени измерения)
                    file.write('{}\t{}\t{}\n'.format(value[0], key.strftime('%Y.%m.%d %H:%M:%S.%f')[:-3], value[1]))
        except Exception as exception:
            print(exception)

        print(f'Генерация тестовых данных окончена. Кол-во устройств: {len(devices)}. Кол-во записей в журнале: {len(journal)}.')


    def _gen_value(self,
                  device: GenDevice,
                  moment: datetime) -> float|None:
        """
        Вычисляется точное значение на момент, затем вносится ошибка измерения
        :param device: Измерительное устройство
        :param moment: Момент измерения
        :return: Результат псевдо-измерения
        """
        if device.unit == 'В':
            voltage = 50.0
            dispersion = 0.0
            return voltage + 2 * (random() - 0.5) * dispersion

        if device.unit == 'А':
            amperage = 5 + 4.95 * math.cos(3 * math.pi * (moment - self.start_time).total_seconds() / self.measurements_duration)
            if device.range_start <= amperage <= device.range_stop:  # Если ампераж входит в доверительный диапазон амперметра
                return amperage  # то возвращаем точное значение
            else:  # иначе вносим ошибку измерения
                dispersion = math.fabs(amperage - (device.range_stop + device.range_start) / 2) / 10
                # Чем сильнее ампераж отлчается от срединного значения диапазона, больше дисперсия
                while True:
                    value = amperage + 2 * (random() - 0.5) * dispersion  # При такой генерации значения могут выйти
                    # за допустимый диапазон, тогда следует повторить генерацию
                    if (0.0 <= value < device.range_start) or (device.range_stop < value <= 10.0):
                        break
                return value

