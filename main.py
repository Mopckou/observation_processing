import os
from configparser import ConfigParser
import matplotlib.pyplot as plt
from src.log import setup_logger
from src.helpers import READER, DIGITAL, ANALOG, TIME, WRITER
from src.finder_gsh import GshOPERATOR
from src.finder_gauss import FinderGauss

setup_logger()

LOG_DIRECTORY = os.path.join(os.getcwd(), 'OUT')

conf = ConfigParser()
conf.read('Configuration.ini')  # читаем конфигурационный файл

FILE = conf.get('FILE', 'file')

reader = READER(FILE)
reader.parse()

reader.cut_observation()  # обрезаем лишние участки когда наблюдение не ведется
reader.filter_digital_observation()  # фильтрация цифровых наблюдений на основе аналогового наблюдения
reader.trim_to_seconds()  # изначально файл в милисекундах, обрезаем файл до секунд
reader.trim_bad_areas()  # удаление нулевых участков
reader.replace_bad_values()

operator = GshOPERATOR()
operator.set_reader(reader)

OBSERVATIONS = [
    DIGITAL.OBSERVATION_6_K1,
    DIGITAL.OBSERVATION_6_K2,
    DIGITAL.OBSERVATION_18_K1,
    DIGITAL.OBSERVATION_18_K2,
    DIGITAL.OBSERVATION_92_K1,
    DIGITAL.OBSERVATION_92_K2,
]

SETUP = {
    DIGITAL.OBSERVATION_6_K1: (1, 25, 80, 0.3),
    DIGITAL.OBSERVATION_6_K2: (1, 25, 80, 0.3),
    DIGITAL.OBSERVATION_18_K1: (1, 100, 140, 0.8),
    DIGITAL.OBSERVATION_18_K2: (1, 100, 140, 0.8),
    DIGITAL.OBSERVATION_92_K1: (80, 150, 320, 0.8),
    DIGITAL.OBSERVATION_92_K2: (80, 150, 320, 0.8)
}


for observation in OBSERVATIONS:

    x = reader.get_array(TIME.T)
    y = reader.get_array(observation)

    original_y = reader.get_original_array(observation)

    observation_name = reader.get_name_observation(observation)
    writer = WRITER(observation_name)

    print(observation_name)
    reader.plot_graph(x, y, observation_name, plt)

    if not reader.meaningful_data(original_y):
        print('Файл %s пустой.' % observation_name)
        continue

    operator.find_gsh(observation)

    if operator.get_result():
        report = operator.get_report()
        print(report)
        writer.nsh_1 = (report['NSH1']['average'], report['NSH1']['sig'])
        writer.nsl_1 = (report['NSL1']['average'], report['NSL1']['sig'])
        writer.nsh_2 = (report['NSH2']['average'], report['NSH2']['sig'])
        writer.nsl_2 = (report['NSL2']['average'], report['NSL2']['sig'])

    finder = FinderGauss(x, y, *SETUP[observation])
    finder.set_plot_manager(plt)
    finder.find_gauss()

    if finder.get_result():
        report = finder.get_report()
        print(report)

        writer.a_sys = report['sys']['average'], report['sys']['sig']
        writer.a_sour = report['sour']['average'], report['sour']['sig']
    writer.write_result()

    finder.prepare_plot(plt)
    reader.plot_graph(x, y, observation_name, plt)

