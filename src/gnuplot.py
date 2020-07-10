import os
import subprocess
from datetime import datetime
from src.helpers import get_all_files_in_dir


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

    def add_plot(self, abscissa, ordinate, line_or_point='lines', lt=4, lw=5, pt=5, ps=0.6, title=''):
        file_name = os.path.join(self.dir, f'model {datetime.utcnow()}.txt')

        with open(file_name, 'w') as f:
            for x, y in zip(abscissa, ordinate):
                f.write(f'{x} {y}\n')

        self.gnuplot.add_plot(file_name, line_or_point, lt, lw, pt, ps, title)

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
        self.clear_dir()


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
        self.__set('term postscript landscape color solid "Times-Roman" 16')
        self.__set('ylabel "Volts"')
        self.__set('xlabel "Seconds"')
        self.__set('key samplen 1 font ",15"')
        self.__set('grid')
        self.__set('key right nobox')
        self.__set('encoding koi8r')

    def set_title(self, name):
        return self.__set(f'title "{name}"')

    def set_out(self, file_name):
        return self.__set(f'out "{file_name}"')

    def set_measure(self, x_measure=100, y_measure=0.1):
        self.__set(f'xtics {x_measure}')
        self.__set(f'ytics {y_measure}')

    def add_plot(self, file_name, line_or_point='lines', lt=4, lw=3, pt=5, ps=0.6, title=''):
        if line_or_point == 'lines':
            plot_setup = f'lt {lt} lw {lw}'
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
