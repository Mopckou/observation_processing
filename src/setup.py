import os
import matplotlib.pyplot as plt
from src.helpers import READER, DIGITAL, ANALOG, TIME, WRITER, OBSERVATIONS, SETUP, OBSERVATION_VIEW
from src.finder_gsh import GshOPERATOR
from src.finder_gauss import FinderGauss
from src.gnuplot import generate_gnuplot_graf, generate_detailed_graf


def observe(file, plot, null, out_dir, setup):
    reader = READER(file)
    reader.parse()

    x = reader.TIME[TIME.T]['array']
    y = reader.OBSERVATION[DIGITAL.OBSERVATION_92_K2]['array']
    if setup['plot_raw_observation']:
        reader.plot_graph(x, y, 'observation_name 92_K2', plt)

    y = reader.OBSERVATION[DIGITAL.OBSERVATION_92_K1]['array']
    if setup['plot_raw_observation']:
        reader.plot_graph(x, y, 'observation_name 92_K1', plt)

    y = reader.OBSERVATION[DIGITAL.OBSERVATION_18_K1]['array']
    if setup['plot_raw_observation']:
        reader.plot_graph(x, y, 'observation_name 18_K1', plt)

    y = reader.OBSERVATION[DIGITAL.OBSERVATION_18_K2]['array']
    if setup['plot_raw_observation']:
        reader.plot_graph(x, y, 'observation_name 18_K2', plt)

    y = reader.OBSERVATION[DIGITAL.OBSERVATION_6_K1]['array']
    if setup['plot_raw_observation']:
        reader.plot_graph(x, y, 'observation_name 6_K1', plt)

    y = reader.OBSERVATION[DIGITAL.OBSERVATION_6_K2]['array']
    if setup['plot_raw_observation']:
        reader.plot_graph(x, y, 'observation_name 6_K2', plt)

    reader.cut_observation()  # обрезаем лишние участки когда наблюдение не ведется
    x = reader.get_time(TIME.T)
    reader.filter_digital_observation()  # фильтрация цифровых наблюдений на основе аналогового наблюдения

    reader.trim_to_seconds()  # изначально файл в милисекундах, обрезаем файл до секунд
    #generate_gnuplot_graf(out_dir, file, ANALOG.OBSERVATION_6_K1, (x, reader.get_array(DIGITAL.OBSERVATION_92_K1)), [], prefix_name='after_time_clearing')
    # generate_gnuplot_graf(out_dir, file, ANALOG.OBSERVATION_6_K1, (x, reader.get_array(DIGITAL.OBSERVATION_92_K2)), [], prefix_name='digital_92k2')
    # generate_gnuplot_graf(out_dir, file, ANALOG.OBSERVATION_6_K1, (x[100:500], reader.get_array(DIGITAL.OBSERVATION_92_K1)[100:500]), [], prefix_name='SOURCE_92k1')
    # generate_gnuplot_graf(out_dir, file, ANALOG.OBSERVATION_6_K1, (x[500:-1000], reader.get_array(DIGITAL.OBSERVATION_92_K2)[500:-1000]), [], prefix_name='bad_areas_2_92k2')

    reader.trim_bad_areas(setup['check_ns'])  # удаление нулевых участков
    reader.trim_bad_dots(setup['check_ns'])
    reader.replace_bad_values()

    for observation in OBSERVATIONS:

        x = reader.get_time(observation)
        y = reader.get_array(observation)

        original_y = reader.get_original_array(observation)

        observation_name = reader.get_name_observation(observation)
        observation_num = observation_name.split('_')[1]  # длина волны наблдения (1.35, 6, 18, 92)
        name = f'CasA_{OBSERVATION_VIEW[observation]}_Volts_obs'

        writer = WRITER(out_dir, name)

        print(observation_name)

        generate_gnuplot_graf(out_dir, file, observation, (x, y), [], 'clear')  # нарисовать чистый график в гнуплоте

        if plot:
            reader.plot_graph(x, y, observation_name, plt)

        if not reader.meaningful_data(observation, y, full_estimate=False):
            print('Файл %s пустой.' % observation_name)
            continue

        ns_finder = GshOPERATOR(reader)
        ns_finder.find_gsh(observation)

        if ns_finder.get_result():
            report = ns_finder.get_report()

            writer.nsh_1 = (report['NSH1']['average'], report['NSH1']['sig'])
            writer.nsl_1 = (report['NSL1']['average'], report['NSL1']['sig'])
            writer.nsh_2 = (report['NSH2']['average'], report['NSH2']['sig'])
            writer.nsl_2 = (report['NSL2']['average'], report['NSL2']['sig'])

        source_finder = FinderGauss(x, y, null[observation_num], *SETUP[observation])
        source_finder.set_plot_manager(plt)
        source_finder.find_gauss()

        if source_finder.get_result():
            report = source_finder.get_report()

            writer.a_sys = report['sys']['average'], report['sys']['sig']
            writer.a_sour = report['sour']['average'], report['sour']['sig']
        writer.write_result(file)

        if plot:
            source_finder.prepare_plot(plt)
            reader.plot_graph(x, y, observation_name, plt)

        all_fits = source_finder.calculate_model_fits() + ns_finder.calculate_model_fits()
        generate_gnuplot_graf(out_dir, file, observation, (x, y), all_fits)
        model_fits = source_finder.calculate_model_fits()
        noise_fits = source_finder.calculate_model_fits(only_source=True)
        # if observation in (DIGITAL.OBSERVATION_92_K1, DIGITAL.OBSERVATION_92_K2):
        #     #noise_fits = source_finder.noise_90cm(model_fits)
        #     noise_fits = source_finder.calculate_model_fits(x=x, many=True, with_source=False)
        #     model_fits = source_finder.calculate_model_fits(x=x, many=True)
        generate_detailed_graf(out_dir, file, observation, (x, y), model_fits, noise_fits)



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
