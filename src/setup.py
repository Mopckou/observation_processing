import os
import datetime
import matplotlib.pyplot as plt
from src.helpers import READER, DIGITAL, ANALOG, TIME, WRITER, OBSERVATIONS, SETUP
from src.finder_gsh import GshOPERATOR
from src.finder_gauss import FinderGauss


def get_files(path):
    try:
        return os.listdir(path)
    except Exception as e:
        pass


def get_all_files_in_dir(path):
    p = path

    if get_files(p) and os.path.exists(p):
        return [os.path.join(p, f) for f in get_files(p)]
    elif get_files(p) is None and os.path.exists(p):
        return [p]


def observe(file, plot, null):
    reader = READER(file)
    reader.parse()

    # x = reader.TIME[TIME.T]['array']
    # y = reader.OBSERVATION[DIGITAL.OBSERVATION_6_K1]['array']
    # reader.plot_graph(x, y, 'observation_name', plt)

    reader.cut_observation()  # обрезаем лишние участки когда наблюдение не ведется
    reader.filter_digital_observation()  # фильтрация цифровых наблюдений на основе аналогового наблюдения
    reader.trim_to_seconds()  # изначально файл в милисекундах, обрезаем файл до секунд

    reader.trim_bad_areas()  # удаление нулевых участков
    reader.trim_bad_dots()
    reader.replace_bad_values()

    operator = GshOPERATOR()
    operator.set_reader(reader)

    for observation in OBSERVATIONS:

        x = reader.get_time(observation)
        y = reader.get_array(observation)

        original_y = reader.get_original_array(observation)

        observation_name = reader.get_name_observation(observation)
        observation_num = observation_name.split('_')[1]  # длина волны наблдения (1.35, 6, 18, 92)

        writer = WRITER(observation_name)

        print(observation_name)
        if plot:
            reader.plot_graph(x, y, observation_name, plt)

        if not reader.meaningful_data(observation, y, full_estimate=False):
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

        finder = FinderGauss(x, y, null[observation_num], *SETUP[observation])
        finder.set_plot_manager(plt)
        finder.find_gauss()

        if finder.get_result():
            report = finder.get_report()
            print(report)

            writer.a_sys = report['sys']['average'], report['sys']['sig']
            writer.a_sour = report['sour']['average'], report['sour']['sig']
        writer.write_result(file)

        if plot:
            finder.prepare_plot(plt)
            reader.plot_graph(x, y, observation_name, plt)


class ShortReport:

    def __init__(self, file_name):
        self.file_name = file_name
        self.prepare_report()

    def write(self, observation, result, description=None):
        self.__write(
            self.__format(observation, result, description)
        )

    def __format(self, observation, result, description):
        bool_translate = {True: 'OK', False: 'FAIL'}
        error_translate = 'Ошибок нет' if description is None else description

        return '{:-<100} {} ({})\n'.format(observation, bool_translate[result], error_translate)

    def __write(self, report, mode='a'):
        with open(self.file_name, mode) as file:
            file.write(report)

    def prepare_report(self):
        self.__write('', 'w')
