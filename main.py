import os
from configparser import ConfigParser
from src.log import setup_logger
from src.setup import observe, ShortReport
from src.helpers import get_all_files_in_dir

setup_logger()

LOG_DIRECTORY = os.path.join(os.getcwd(), 'OUT')

conf = ConfigParser()
conf.read('Configuration.ini')  # читаем конфигурационный файл
report_name = 'short_report.txt'

path = conf.get('FILE', 'file')
plot = int(conf.get('GENERAL', 'plot'))
null = {
    '1.35': float(conf.get('NULL', 'K')),
    '6': float(conf.get('NULL', 'C')),
    '18': float(conf.get('NULL', 'L')),
    '92': float(conf.get('NULL', 'P')),
}
out_dir = conf.get('OUT', 'dir')
report = ShortReport(report_name)
setup = {
    'check_ns': bool(conf.get('GENERAL', 'check_ns')),
    'plot_raw_observation': int(conf.get('GENERAL', 'plot_raw_observation')),
    'hands_input': int(conf.get('GENERAL', 'hands_input_observation_window')),
    'restoring_observation_sequence': int(conf.get('GENERAL', 'restoring_observation_sequence')),
    'renumerate_time_column': int(conf.get("GENERAL", 'renumerate_time_column'))
}

for file in get_all_files_in_dir(path):
    try:
        observe(file, plot, null, out_dir, setup)
    except Exception as e:
        report.write(file, False, e)
        print(e)
        continue

    report.write(file, True)
