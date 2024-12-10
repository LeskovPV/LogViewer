from dataclasses import dataclass
from datetime import timedelta, datetime


@dataclass
class Record:
    """Запись в журнале"""

    ip_addr: str
    """Адрес устройства"""

    moment: datetime
    """Начало диапазона"""

    value: float
    """Ед.изм."""


@dataclass
class Device:
    """Измерительное устройство"""

    ip_addr: str
    """Адрес"""

    range_start: float
    """Начало диапазона"""

    range_stop: float
    """Конец диапазона"""

    unit: str
    """Ед.изм."""


@dataclass
class GenDevice(Device):
    """Измерительное устройство, используемое для генерации"""

    start_time: datetime
    """Время начала работы""" # у каждого устройства немного разное

    time_step: timedelta
    """Временной шаг (в сек.) между измерениями"""  # у каждого устройства немного разное