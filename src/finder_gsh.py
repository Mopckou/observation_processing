import scipy
import logging
import matplotlib.pyplot as plt
from src.helpers import GshB, GshH, ANALOG, DIGITAL, INTERPRETER

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
        self.report = {}
        self.plots = []
        self.gsh_B = {}
        self.gsh_H = {}
        self.indent = 2  # отступ от края ГША, чтобы не учитывать время на выход на уровень

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
            if not result:
                raise ErrorVerifyGSHA

    def set_ordinate(self, array):
        self.ordinate = array

    def set_abscissa(self, array):
        self.abscissa = array

    def run(self):
        try:
            self.check_gsha()
        except ErrorVerifyGSHA:
            self.__set_result(False, 'Недопустимое количество включений ГША!')
            return
        except Exception as e:
            logger.exception(e)
            self.__set_result(False, 'Ошибка в ходе проверки ГША!')
            return

        try:
            self.calc_nsh(channel=1)
            self.calc_nsh(channel=2)

            self.calc_nsl(channel=1)
            self.calc_nsl(channel=2)
        except Exception as e:
            logger.exception(e)
            self.__set_result(False, 'Ошибка в обработке наблюдения!')
        else:
            self.__set_result(True, 'Ошибок нет.')

    def calc_nsh(self, channel):
        nsh = self.NSH[channel]

        self.report[nsh] = {}
        gsh = self.gsh_B[channel]['array']

        average, sig = self.__calc(gsh)

        self.report[nsh]['average'] = average
        self.report[nsh]['sig'] = sig

    def calc_nsl(self, channel):
        nsl = self.NSL[channel]

        self.report[nsl] = {}
        gsh = self.gsh_H[channel]['array']

        average, sig = self.__calc(gsh)

        self.report[nsl]['average'] = average
        self.report[nsl]['sig'] = sig

    def __calc(self, array):
        marks = INTERPRETER.get_single_intervals(array)

        averages = []
        for num, val in enumerate(marks):
            begin = val['begin'] + self.indent
            end = val['end']# - self.indent
            sector_y = self.ordinate[begin:end]
            sector_x = self.abscissa[begin:end]

            sector_average = INTERPRETER.get_average(sector_y)

            new_sector_y = self.__get_new_sector(sector_y, sector_average)  # пересчитанный сектор, с средним значением
            self._append_plot(sector_x, new_sector_y)

            averages.append(sector_average)

        _average = INTERPRETER.get_average(averages)
        sigma = self.get_sigma(averages)
        percent = self.get_percent(sigma, _average)

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

    @staticmethod
    def get_sigma(array):
        sigma = 0.
        count = len(array)
        average = INTERPRETER.get_average(array)

        for value in array:
            sigma += (value - average) * (value - average)
        sigma = sigma / (count - 1)
        sigma = scipy.sqrt(sigma)
        return sigma

    @staticmethod
    def get_percent(error, average):
        if average == 0.:
            return

        return error * 100 / average

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

    def __set_result(self, result, description):
        self.__result = result
        self.__description = description

    def get_result(self):
        return self.__result

    def get_description(self):
        return self.__description

    def write_result(self):
        pass
