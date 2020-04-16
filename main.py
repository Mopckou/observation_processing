import os
from configparser import ConfigParser
from src.log import setup_logger
from src.setup import observe, get_all_files_in_dir, ShortReport

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
report = ShortReport(report_name)

for file in get_all_files_in_dir(path):
    try:
        observe(file, plot, null)
    except Exception as e:
        report.write(file, False, e)
        continue

    report.write(file, True)
