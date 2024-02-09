import scipy
import logging
import matplotlib.pyplot as plt
from src.helpers import INTERPRETER, GshB, GshH, DIGITAL, ANALOG, TIME, TABLE

logger = logging.getLogger('LOG')


class ErrorVerifyGSHA(Exception):
    pass


class FinderGsh:
    NSH = {1: 'NSH1', 2: 'NSH2'}
    NSL = {1: 'NSL1', 2: 'NSL2'}

    def __init__(self, pyplot=None):
        if pyplot is None:
            self.plt = plt
        else:
            self.plt = pyplot
        self.__result = None
        self.__description = ''
        self.ordinate = []
        self.abscissa = []
        self.__report = {}
        self.plots = []
        self.gsh_B = {}
        self.gsh_H = {}
        self.indent = 1  # отступ от края ГША, чтобы не учитывать время на выход на уровень
        self.width_edge = 1
        self.real_plot = False

    def set_gsh_H(self, table, channel, array):
        self.gsh_H[channel] = {
                    'table': table,
                    'array': array
                }

    def set_gsh_B(self, table, channel, array):
        self.gsh_B[channel] = {
                    'table': table,
                    'array': array
                }

    @staticmethod
    def verify(obj):
        array = obj['array']
        table = obj['table']
        logger.info('ПРОВЕРКА МАССИВА НА КОРРЕКТНОЕ КОЛИЧЕСТВО ГША. НОМЕР СТОЛБЦА - %s' % table)

        count = INTERPRETER.count_on_interval(array)
        logger.info('Количество ГША - %s' % count)

        result = count == 2 or count == 1
        logger.info('Результат проверки - %s' % result)
        return result

    def check_gsha(self):
        self.__check_gsha(self.gsh_H)
        self.__check_gsha(self.gsh_B)

    def __check_gsha(self, gsha):
        for value in gsha:
            obj = gsha[value]
            result = self.verify(obj)
            # TODO раскоментить
            # if not result:
            #     raise ErrorVerifyGSHA

    def set_ordinate(self, array):
        self.ordinate = array

    def set_abscissa(self, array):
        self.abscissa = array

    def run(self):
        try:
            self.check_gsha()
        except ErrorVerifyGSHA:
            self.__set_result(False, 'Недопустимое количество включений ГША!')
            print('ОШИБКА')
            return

        except Exception as e:
            logger.exception(e)
            self.__set_result(False, 'Ошибка в ходе проверки ГША!')
            print('ОШИБКА')
            return

        self.calc_nsh(channel=1)
        self.calc_nsh(channel=2)

        self.calc_nsl(channel=1)
        self.calc_nsl(channel=2)
        self.__set_result(True, 'Ошибок нет.')


    def calc_nsh(self, channel):
        nsh = self.NSH[channel]

        self.__report[nsh] = {}
        gsh = self.gsh_B[channel]['array']

        try:
            average, sig = self.__calc(gsh)
        except Exception as e:
            logger.exception(e)
            self.__report[nsh]['average'] = 0
            self.__report[nsh]['sig'] = 0
            return

        if sig > 60 or sig < 0:
            average, sig = 0.0, 0.0

        self.__report[nsh]['average'] = average
        self.__report[nsh]['sig'] = sig

    def calc_nsl(self, channel):
        nsl = self.NSL[channel]

        self.__report[nsl] = {}
        gsh = self.gsh_H[channel]['array']

        try:
            average, sig = self.__calc(gsh)
        except Exception as e:
            logger.exception(e)
            self.__report[nsl]['average'] = 0
            self.__report[nsl]['sig'] = 0
            return

        if sig > 60 or sig < 0:
            average, sig = 0.0, 0.0

        self.__report[nsl]['average'] = average
        self.__report[nsl]['sig'] = sig

    def __calc(self, array):
        marks = INTERPRETER.get_single_intervals(array)

        averages = []
        for num, val in enumerate(marks):
            begin = val['begin']
            end = val['end']
            sector_y = self.ordinate[begin + self.indent:end]
            sector_x = self.abscissa[begin + self.indent:end]

            right_edge_y = self.ordinate[begin - self.width_edge - self.indent:begin - self.indent]
            right_edge_x = self.abscissa[begin - self.width_edge - self.indent:begin - self.indent]

            left_edge_y = self.ordinate[end + self.indent:end + self.indent + self.width_edge]
            left_edge_x = self.abscissa[end + self.indent:end + self.indent + self.width_edge]

            sector_average = INTERPRETER.get_average(sector_y)
            average_right_edge = INTERPRETER.get_average(right_edge_y)
            average_left_edge = INTERPRETER.get_average(left_edge_y)
            base = INTERPRETER.get_average([average_right_edge, average_left_edge])

            amplitude = sector_average - base

            new_sector_y = self.__get_new_sector(sector_y, sector_average)  # пересчитанный сектор, с средним значением
            new_right_edge_y = self.__get_new_sector(right_edge_y, average_right_edge)
            new_left_edge_y = self.__get_new_sector(left_edge_y, average_left_edge)

            if not self.real_plot:  # для красивого графика уберем отступ от включения ГШ
                sector_x = self.abscissa[begin:end]
                sector_y = self.ordinate[begin:end]
                new_sector_y = self.__get_new_sector(sector_y, sector_average)
                right_edge_y = self.ordinate[begin - self.width_edge - self.indent:begin]
                right_edge_x = self.abscissa[begin - self.width_edge - self.indent:begin]

                left_edge_y = self.ordinate[end:end + self.indent + self.width_edge]
                left_edge_x = self.abscissa[end:end + self.indent + self.width_edge]

                new_right_edge_y = self.__get_new_sector(right_edge_y, average_right_edge)
                new_left_edge_y = self.__get_new_sector(left_edge_y, average_left_edge)

            self._append_plot(
                right_edge_x + sector_x + left_edge_x,
                new_right_edge_y + new_sector_y + new_left_edge_y
            )

            averages.append(amplitude)

        if len(averages) == 0:
            return -1, -1

        if len(averages) == 1:
            return averages[0], 0

        _average = INTERPRETER.get_average(averages)
        sigma = INTERPRETER.get_sigma(averages)
        percent = INTERPRETER.get_percent(sigma, _average)

        return _average, percent

    def __get_new_sector(self, old_sector, average):
        new_sector = []
        for i in old_sector:
            new_sector.append(average)
        return new_sector

    def _append_plot(self, x, y):
        self.plots.append(
            [x, y]
        )

    def build_graph(self):
        x = self.abscissa
        y = self.ordinate
        self.plt.scatter(x, y, s=5)

        for x, y in self.plots:
            self.plt.plot(
               x, y
            )

        self.plt.xlabel(r'$x$')
        self.plt.ylabel(r'$f(y)$')
        self.plt.title(r'$y=$')
        self.plt.grid(True)
        self.plt.show()

    def calculate_model_fits(self):
        return [(x, y) for x, y in self.plots]

    def prepare_plot(self):
        for x, y in self.calculate_model_fits():
            self.plt.plot(
               x, y
            )

    def __set_result(self, result, description):
        self.__result = result
        self.__description = description

    def get_result(self):
        return self.__result

    def get_description(self):
        return self.__description

    def get_report(self):
        return self.__report


class GshOPERATOR:

    def __init__(self, reader):
        self.__result = False
        self.__description = ''
        self.__report = []
        self.finder_gsh = FinderGsh()
        self.reader = reader

    def set_reader(self, reader):
        self.reader = reader

    def find_gsh(self, observation):
        self.finder_gsh.indent = 2

        gsh = TABLE[observation]

        self.finder_gsh.set_ordinate(self.reader.get_array(observation))
        self.finder_gsh.set_abscissa(self.reader.get_time(observation))

        self.finder_gsh.set_gsh_B(gsh['GSH_B_K1'], 1, self.reader.get_array(gsh['GSH_B_K1']))
        self.finder_gsh.set_gsh_B(gsh['GSH_B_K2'], 2, self.reader.get_array(gsh['GSH_B_K2']))

        self.finder_gsh.set_gsh_H(gsh['GSH_H_K1'], 1, self.reader.get_array(gsh['GSH_H_K1']))
        self.finder_gsh.set_gsh_H(gsh['GSH_H_K2'], 2, self.reader.get_array(gsh['GSH_H_K2']))

        self.finder_gsh.run()

        self.__description = self.finder_gsh.get_description()
        self.__result = self.finder_gsh.get_result()
        self.__report = self.finder_gsh.get_report()

        self.finder_gsh.prepare_plot()

    def calculate_model_fits(self):
        return self.finder_gsh.calculate_model_fits()

    def get_description(self):
        return self.__description

    def get_result(self):
        return self.__result

    def get_report(self):
        return self.__report
