# coding=utf-8
import sys


from tools.log_viewer import LogViewer
# from tools.log_generator import LogGenerator

if __name__ == "__main__":
    # LogGenerator().generate()  # Генерация тестовых данных (см. LogGenerator._gen_value)
    LogViewer().view(**dict(zip(['this_file', 'cfg_file', 'log_file'], sys.argv)))

