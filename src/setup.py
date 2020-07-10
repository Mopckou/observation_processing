import os
import matplotlib.pyplot as plt
from src.helpers import READER, DIGITAL, ANALOG, TIME, WRITER, OBSERVATIONS, SETUP, OBSERVATION_VIEW, generate_portion
from src.finder_gsh import GshOPERATOR
from src.finder_gauss import FinderGauss
from src.gnuplot import GnuplotHelper


def observe(file, plot, null, out_dir):
    reader = READER(file)
    reader.parse()
    # import subprocess
    # try:
    #     sp = subprocess.run(['gnuplot', '--version'], shell=True, check=True, stdout=subprocess.PIPE)
    #     print(sp.stdout, 'вывод')
    # except subprocess.CalledProcessError:
    #     print('Установите gnuplot!')
    #
    #
    #
    # exit()
    x = reader.TIME[TIME.T]['array']
    y = reader.OBSERVATION[DIGITAL.OBSERVATION_92_K2]['array']
    #reader.plot_graph(x, y, 'observation_name', plt)

    y = reader.OBSERVATION[DIGITAL.OBSERVATION_92_K1]['array']
    #reader.plot_graph(x, y, 'observation_name', plt)


    y = reader.OBSERVATION[DIGITAL.OBSERVATION_18_K1]['array']
    #reader.plot_graph(x, y, 'observation_name', plt)

    y = reader.OBSERVATION[DIGITAL.OBSERVATION_18_K2]['array']
    #reader.plot_graph(x, y, 'observation_name', plt)

    y = reader.OBSERVATION[DIGITAL.OBSERVATION_6_K1]['array']
    #reader.plot_graph(x, y, 'observation_name', plt)

    y = reader.OBSERVATION[DIGITAL.OBSERVATION_6_K2]['array']
    #reader.plot_graph(x, y, 'observation_name', plt)

    #reader.cut_other_observation()
    # g = GnuplotHelper()
    # g.set_title('stage 1')
    # g.add_plot(x, y, 'points', title='92cm - P2')
    # g.plot()
    reader.cut_observation()  # обрезаем лишние участки когда наблюдение не ведется
    new_x = reader.get_array(TIME.T)
    new_y = reader.get_array(DIGITAL.OBSERVATION_92_K2)
    # g = GnuplotHelper()
    # g.set_title('stage 2')
    # g.add_plot(new_x, new_y, 'points', title='92cm - P2')
    # g.plot()

    reader.filter_digital_observation()  # фильтрация цифровых наблюдений на основе аналогового наблюдения
    reader.trim_to_seconds()  # изначально файл в милисекундах, обрезаем файл до секунд

    reader.trim_bad_areas()  # удаление нулевых участков
    reader.trim_bad_dots()
    reader.replace_bad_values()
    new_x = reader.get_array(TIME.T)
    new_y = reader.get_array(DIGITAL.OBSERVATION_92_K2)

    # g = GnuplotHelper()
    # g.set_title('stage 3')
    # g.add_plot(new_x, new_y, 'points', title='92cm - P2')
    # g.plot()
    for observation in OBSERVATIONS:

        x = reader.get_time(observation)
        y = reader.get_array(observation)

        original_y = reader.get_original_array(observation)

        # # TODO удалить
        # if observation == DIGITAL.OBSERVATION_18_K1:
        #     continue

        observation_name = reader.get_name_observation(observation)
        observation_num = observation_name.split('_')[1]  # длина волны наблдения (1.35, 6, 18, 92)
        name = f'CasA_{OBSERVATION_VIEW[observation]}_Volts_obs'

        writer = WRITER(name)

        print(observation_name)

        if plot:
            reader.plot_graph(x, y, observation_name, plt)

        if not reader.meaningful_data(observation, y, full_estimate=False):
            print('Файл %s пустой.' % observation_name)
            continue

        ns_finder = GshOPERATOR(reader)
        ns_finder.find_gsh(observation)

        if ns_finder.get_result():
            report = ns_finder.get_report()
            print(report)
            writer.nsh_1 = (report['NSH1']['average'], report['NSH1']['sig'])
            writer.nsl_1 = (report['NSL1']['average'], report['NSL1']['sig'])
            writer.nsh_2 = (report['NSH2']['average'], report['NSH2']['sig'])
            writer.nsl_2 = (report['NSL2']['average'], report['NSL2']['sig'])

        source_finder = FinderGauss(x, y, null[observation_num], *SETUP[observation])
        source_finder.set_plot_manager(plt)
        source_finder.find_gauss()

        if source_finder.get_result():
            report = source_finder.get_report()
            print(report)

            writer.a_sys = report['sys']['average'], report['sys']['sig']
            writer.a_sour = report['sour']['average'], report['sour']['sig']
        writer.write_result(file)

        if plot:
            source_finder.prepare_plot(plt)
            reader.plot_graph(x, y, observation_name, plt)

        all_fits = source_finder.calculate_model_fits() + ns_finder.calculate_model_fits()
        generate_gnuplot_graf(out_dir, file, observation, (x, y), all_fits)
        model_fits = source_finder.calculate_model_fits()
        noise_fits = source_finder.calculate_model_fits(with_source=False)
        # if observation in (DIGITAL.OBSERVATION_92_K1, DIGITAL.OBSERVATION_92_K2):
        #     #noise_fits = source_finder.noise_90cm(model_fits)
        #     noise_fits = source_finder.calculate_model_fits(x=x, many=True, with_source=False)
        #     model_fits = source_finder.calculate_model_fits(x=x, many=True)

        generate_detailed_graf(out_dir, file, observation, (x, y), model_fits, noise_fits)


def generate_gnuplot_graf(out_dir, file, observation, experiment, all_fits):
    *_, file_name = os.path.split(file)
    name_without_underscore = file_name.replace("_", " ")  # title
    name_without_extension = file_name.split(".")[0]
    observation_view = OBSERVATION_VIEW[observation]

    path = os.path.join(out_dir, 'gnuplot', name_without_extension)
    if not os.path.exists(path):
        os.makedirs(path)

    g = GnuplotHelper()
    g.set_title(name_without_underscore)
    g.set_out(os.path.join(path, f'{observation_view}.ps'))
    g.add_plot(*experiment, 'points', title=observation_view)

    for abscissa, ordinate in all_fits:
        g.add_plot(abscissa, ordinate)
    g.plot()


def generate_detailed_graf(out_dir, file, observation, experiment, fits, noise_fits):
    *_, file_name = os.path.split(file)
    name_without_underscore = file_name.replace("_", " ")  # title
    name_without_extension = file_name.split(".")[0]
    observation_view = OBSERVATION_VIEW[observation]

    path = os.path.join(out_dir, 'gnuplot', name_without_extension)
    if not os.path.exists(path):
        os.makedirs(path)

    g = GnuplotHelper()
    g.set_out(os.path.join(path, f'detailed {observation_view}.ps'))
    x, y = experiment
    g.set_mesure(100, 0.1)
    new_fits = list(zip(fits, noise_fits))
    for portion in generate_portion(new_fits, 4):
        g.set_multiplot(2, 2, title=name_without_underscore)
        for key, value in enumerate(portion, 1):
            source, noise = value
            abscissa, ordinate = source
            # TODO
            # begin, end = abscissa[0] - 20, abscissa[-1] + 20
            # if key == 4:
            #     break

            # breakpoint()
            begin, end = abscissa[0] - 20, abscissa[-1] + 20
            begin_index, end_index = x.index(begin), x.index(end)
            new_x, new_y = x[begin_index: end_index + 1], y[begin_index: end_index + 1]
            g.add_plot(new_x, new_y, 'point', title=f'{observation_view}')
            g.add_plot(abscissa, ordinate, title=f'model')
            g.add_plot(*noise, title='')
            g.form_plot()
        g.set_end_multiplot()

    g.plot()


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
