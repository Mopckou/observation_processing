import os
import subprocess
from datetime import datetime
from src.helpers import get_all_files_in_dir, OBSERVATION_VIEW, generate_portion
from random import randint


class GnuplotHelper:

    def __init__(self, sub_dir=''):
        self.gnuplot = Gnuplot()
        self.dir = 'tmp/'
        self.out_name = f'graf {datetime.utcnow()}.ps'
        self.title_name = ''
        self.multiplot = ''
        self.measure = ''

        if sub_dir:
            self.dir = os.path.join(sub_dir, 'tmp/')

        self.create_dir(self.dir)

    def default_setup(self):
        self.gnuplot.default_setup()

    @staticmethod
    def create_dir(path):
        if not os.path.exists(path):
            os.makedirs(path)

    def set_out(self, out_name):
        self.out_name = out_name

    def set_title(self, title_name):
        self.title_name = title_name

    def set_mesure(self, x_measure, y_measure):
        self.measure = [x_measure, y_measure]

    def clear_dir(self):
        for f in get_all_files_in_dir(self.dir):
            os.remove(f)

    def add_plot(self, abscissa, ordinate, line_or_point='lines', lt=4, lw=5, pt=5, ps=0.6, random_color=None, title=''):
        file_name = os.path.join(self.dir, f'model {datetime.utcnow()}.txt')

        with open(file_name, 'w') as f:
            for x, y in zip(abscissa, ordinate):
                f.write(f'{x} {y}\n')

        self.gnuplot.add_plot(file_name, line_or_point, lt, lw, pt, ps, random_color, title)

    def form_plot(self):
        self.gnuplot.form_plot()

    def set_multiplot(self, lines, rows, scale_x=1, scale_y=1, offset_x=0, offset_y=0, title=''):
        self.gnuplot.set_multiplot(
            f'set multiplot '
            f'title "{title}" '
            f'layout {lines}, {rows} '
            f'scale {scale_x}, {scale_y} '
            f'offset {offset_x}, {offset_y} \n'
        )

    def set_end_multiplot(self):
        self.gnuplot.set_end_multiplot()

    def plot(self):
        self.default_setup()
        self.gnuplot.set_out(self.out_name)
        self.gnuplot.set_title(self.title_name)
        if self.measure:
            self.gnuplot.set_measure(*self.measure)
        if self.multiplot:
            self.gnuplot.set_multiplot(self.multiplot)
        self.gnuplot.plot()
        # TODO удалить try: exc
        try:
            self.clear_dir()
        except Exception as e:
            print(e)


class Gnuplot:

    def __init__(self):
        self.plot_data = ''
        self.__query = ''
        self.multiplot = False
        self.__plots = ''
        self.measure = []

    def __set(self, query):
        return self.__add('set ' + query)

    def __add(self, query):
        self.__query += query + '\n'

    def __run(self, query):
        sp = subprocess.Popen(
            'gnuplot',
            shell=False,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        return sp.communicate(
            query.encode()
        )

    def default_setup(self):
        self.__add('unset key')
        self.__set('term postscript landscape color solid "Times-Roman" 24')
        self.__set('ylabel "Volts"')
        self.__set('xlabel "Seconds"')
        self.__set('key samplen 1 font ",20"')
        self.__set('grid')
        self.__set('key right nobox')
        self.__set('encoding koi8r')

    def set_title(self, name):
        return self.__set(f'title "{name}"')

    def set_out(self, file_name):
        return self.__set(f'out "{file_name}"')

    def set_xrange(self, xrange):
        return self.__set(f'xrange [{xrange[0]}:{xrange[1]}]')

    def set_measure(self, x_measure=100, y_measure=0.1):
        self.__set(f'xtics {x_measure}')
        self.__set(f'ytics {y_measure}')

    def add_plot(self, file_name, line_or_point='lines', lt=4, lw=3, pt=5, ps=0.6, random_color=None, title=''):
        if line_or_point == 'lines':
            plot_setup = f'lt {lt} lw {lw} {"lc " + str(randint(1, 10)) if random_color else ""}'
        else:
            plot_setup = f'pt {pt} ps {ps}'

        self.plot_data += f'"{file_name}" with {line_or_point} ' + plot_setup + f' title "{title}", '

    def form_plot(self):
        if not self.plot_data:
            return

        self.__plots += 'plot ' + self.plot_data + '\n'
        self.plot_data = ''

    def set_end_multiplot(self):
        self.__plots += 'unset multiplot\n'

    def set_multiplot(self, setup_multiplot):
        self.__plots += setup_multiplot
        #self.multiplot = True

    def plot(self):
        self.form_plot()
        self.__add(self.__plots)

        # if self.multiplot:
        #     self.__add('unset multiplot\n')

        print('___')
        print(self.__query)
        print('___')

        return self.__run(self.__query)

    @staticmethod
    def check_gnuplot(end=False):
        try:
            subprocess.run(['gnuplot', '--version'], shell=False, stdout=subprocess.PIPE)
        except subprocess.CalledProcessError:
            print('Установите gnuplot! Или выключите генерацию графиков в конфиге!')
            if end:
                exit()
            return False
        except Exception as e:
            print(e)
            raise

        return True


def generate_gnuplot_graf(out_dir, file, observation, experiment, all_fits, prefix_name='', range=None):
    *_, file_name = os.path.split(file)
    name_without_underscore = file_name.replace("_", " ")  # title
    name_without_extension = file_name.split(".")[0]
    observation_view = OBSERVATION_VIEW.get(observation, '')

    path = os.path.join(out_dir, 'gnuplot', name_without_extension)
    if not os.path.exists(path):
        os.makedirs(path)

    g = GnuplotHelper()
    g.set_title(name_without_underscore)
    g.set_out(os.path.join(path, f'{prefix_name} {observation_view}.ps'))
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
            begin, end = abscissa[0] - 10, abscissa[-1] + 10
            begin_index, end_index = x.index(begin), x.index(end)
            new_x, new_y = x[begin_index: end_index + 1], y[begin_index: end_index + 1]
            g.add_plot(new_x, new_y, 'point', title=f'{observation_view}')
            g.add_plot(abscissa, ordinate, title=f'model')
            g.add_plot(*noise, title='')
            g.form_plot()
        g.set_end_multiplot()

    g.plot()
