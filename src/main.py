# coding=utf-8
import sys


from tools.log_loader import LogLoader
# from tools.log_generator import LogGenerator

if __name__ == "__main__":
    # LogGenerator().generate()  # Генерация тестовых данных (см. LogGenerator._gen_value)
    LogLoader().load(**dict(zip(['this_file', 'cfg_file', 'log_file'], sys.argv)))
