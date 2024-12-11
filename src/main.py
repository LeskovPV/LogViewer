# coding=utf-8
import os
import sys


from tools.log_loader import LogLoader
# from tools.log_generator import LogGenerator

if __name__ == "__main__":
    # LogGenerator().generate()
    load_kwargs = dict()
    position = 0  # Счётчик позиций аргументов командной строки
    for arg in sys.argv:
        if os.path.exists(arg):
            if position == 1:
                load_kwargs.update(cfg_file = arg)
            if position == 2:
                load_kwargs.update(log_file = arg)
        position += 1

    LogLoader().load(**load_kwargs)
