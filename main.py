import os
from configparser import ConfigParser
import matplotlib.pyplot as plt
from src.log import setup_logger
from src.helpers import READER, DIGITAL, ANALOG, TIME
from src.finder_gsh import OPERATOR
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

operator = OPERATOR()
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
    DIGITAL.OBSERVATION_6_K1: (1, 25, 100, 0.3),
    DIGITAL.OBSERVATION_6_K2: (1, 25, 100, 0.3),
    DIGITAL.OBSERVATION_18_K1: (1, 100, 140, 0.8),
    DIGITAL.OBSERVATION_18_K2: (1, 100, 140, 0.8),
    DIGITAL.OBSERVATION_92_K1: (80, 150, 320, 0.8),
    DIGITAL.OBSERVATION_92_K2: (80, 150, 320, 0.8)
}


for observation in OBSERVATIONS:

    operator.calc_gsha(observation)

    if operator.get_result():
        operator.get_resport()

    x = reader.get_array(TIME.T)
    y = reader.get_array(observation)
    print(*SETUP[observation])

    finder = FinderGauss(x, y, *SETUP[observation])  # 6cm
    input()
    finder.set_plot_manager(plt)
    finder.run()

    if finder.get_result():
        finder.get_report()
