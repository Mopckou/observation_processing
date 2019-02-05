import scipy
import logging
import matplotlib.pyplot as plt
from src.helpers import INTERPRETER, GshB, GshH, DIGITAL, ANALOG, TIME

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
        self.indent = 2  # отступ от края ГША, чтобы не учитывать время на выход на уровень
        self.width_edge = 5

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

        self.__report[nsh] = {}
        gsh = self.gsh_B[channel]['array']

        average, sig = self.__calc(gsh)

        self.__report[nsh]['average'] = average
        self.__report[nsh]['sig'] = sig

    def calc_nsl(self, channel):
        nsl = self.NSL[channel]

        self.__report[nsl] = {}
        gsh = self.gsh_H[channel]['array']

        average, sig = self.__calc(gsh)

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

            right_edge_y = self.ordinate[begin - self.width_edge:begin]
            right_edge_x = self.abscissa[begin - self.width_edge:begin]

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

            self._append_plot(sector_x, new_sector_y)
            self._append_plot(right_edge_x, new_right_edge_y)
            self._append_plot(left_edge_x, new_left_edge_y)

            averages.append(amplitude)

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
    TABLE = {
        ANALOG.OBSERVATION_6_K1: {
            'GSH_B_K1': GshB.GSH_B_6_K1,
            'GSH_B_K2': GshB.GSH_B_6_K2,
            'GSH_H_K1': GshH.GSH_H_6_K1,
            'GSH_H_K2': GshH.GSH_H_6_K2
        },

        ANALOG.OBSERVATION_6_K2: {
            'GSH_B_K1': GshB.GSH_B_6_K1,
            'GSH_B_K2': GshB.GSH_B_6_K2,
            'GSH_H_K1': GshH.GSH_H_6_K1,
            'GSH_H_K2': GshH.GSH_H_6_K2
        },

        ANALOG.OBSERVATION_18_K1: {
            'GSH_B_K1': GshB.GSH_B_18_K1,
            'GSH_B_K2': GshB.GSH_B_18_K2,
            'GSH_H_K1': GshH.GSH_H_18_K1,
            'GSH_H_K2': GshH.GSH_H_18_K2
        },

        ANALOG.OBSERVATION_18_K2: {
            'GSH_B_K1': GshB.GSH_B_18_K1,
            'GSH_B_K2': GshB.GSH_B_18_K2,
            'GSH_H_K1': GshH.GSH_H_18_K1,
            'GSH_H_K2': GshH.GSH_H_18_K2
        },

        ANALOG.OBSERVATION_92_K1: {
            'GSH_B_K1': GshB.GSH_B_92_K1,
            'GSH_B_K2': GshB.GSH_B_92_K2,
            'GSH_H_K1': GshH.GSH_H_92_K1,
            'GSH_H_K2': GshH.GSH_H_92_K2
        },

        ANALOG.OBSERVATION_92_K2: {
            'GSH_B_K1': GshB.GSH_B_92_K1,
            'GSH_B_K2': GshB.GSH_B_92_K2,
            'GSH_H_K1': GshH.GSH_H_92_K1,
            'GSH_H_K2': GshH.GSH_H_92_K2
        },

        DIGITAL.OBSERVATION_6_K1: {
            'GSH_B_K1': GshB.GSH_B_6_K1,
            'GSH_B_K2': GshB.GSH_B_6_K2,
            'GSH_H_K1': GshH.GSH_H_6_K1,
            'GSH_H_K2': GshH.GSH_H_6_K2
        },

        DIGITAL.OBSERVATION_6_K2: {
            'GSH_B_K1': GshB.GSH_B_6_K1,
            'GSH_B_K2': GshB.GSH_B_6_K2,
            'GSH_H_K1': GshH.GSH_H_6_K1,
            'GSH_H_K2': GshH.GSH_H_6_K2
        },

        DIGITAL.OBSERVATION_18_K1: {
            'GSH_B_K1': GshB.GSH_B_18_K1,
            'GSH_B_K2': GshB.GSH_B_18_K2,
            'GSH_H_K1': GshH.GSH_H_18_K1,
            'GSH_H_K2': GshH.GSH_H_18_K2
        },

        DIGITAL.OBSERVATION_18_K2: {
            'GSH_B_K1': GshB.GSH_B_18_K1,
            'GSH_B_K2': GshB.GSH_B_18_K2,
            'GSH_H_K1': GshH.GSH_H_18_K1,
            'GSH_H_K2': GshH.GSH_H_18_K2
        },

        DIGITAL.OBSERVATION_92_K1: {
            'GSH_B_K1': GshB.GSH_B_92_K1,
            'GSH_B_K2': GshB.GSH_B_92_K2,
            'GSH_H_K1': GshH.GSH_H_92_K1,
            'GSH_H_K2': GshH.GSH_H_92_K2
        },

        DIGITAL.OBSERVATION_92_K2: {
            'GSH_B_K1': GshB.GSH_B_92_K1,
            'GSH_B_K2': GshB.GSH_B_92_K2,
            'GSH_H_K1': GshH.GSH_H_92_K1,
            'GSH_H_K2': GshH.GSH_H_92_K2
        },
    }

    def __init__(self):
        self.__result = False
        self.__description = ''
        self.__report = []
        self.reader = None

    def set_reader(self, reader):
        self.reader = reader

    def find_gsh(self, observation):
        parser = FinderGsh()
        #parser.indent = 2

        gsh = self.TABLE[observation]

        parser.set_ordinate(self.reader.get_array(observation))
        parser.set_abscissa(self.reader.get_array(TIME.T))

        parser.set_gsh_B(gsh['GSH_B_K1'], 1, self.reader.get_array(gsh['GSH_B_K1']))
        parser.set_gsh_B(gsh['GSH_B_K2'], 2, self.reader.get_array(gsh['GSH_B_K2']))

        parser.set_gsh_H(gsh['GSH_H_K1'], 1, self.reader.get_array(gsh['GSH_H_K1']))
        parser.set_gsh_H(gsh['GSH_H_K2'], 2, self.reader.get_array(gsh['GSH_H_K2']))

        parser.run()

        self.__description = parser.get_description()
        self.__result = parser.get_result()
        self.__report = parser.get_report()

        parser.build_graph()

    def get_description(self):
        return self.__description

    def get_result(self):
        return self.__result

    def get_report(self):
        return self.__report

if __name__ == '__main__':



    a = [{'count': 0.30215609}, {'count': 0.44846553}, {'count': 0.43828237}, {'count': 0.44720364}, {'count': 0.43806744}]

    print(__get_excess_elements(a))