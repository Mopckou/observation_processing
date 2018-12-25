import copy
import logging

logger = logging.getLogger('LOG')


class TIME:
    T = 1


class ANALOG:
    OBSERVATION_6_K1_A = 6
    OBSERVATION_6_K2_A = 7
    OBSERVATION_18_K1_A = 8
    OBSERVATION_18_K2_A = 9
    OBSERVATION_92_K1_A = 10
    OBSERVATION_92_K2_A = 11


class DIGITAL:
    OBSERVATION_6_K1_C = 14
    OBSERVATION_6_K2_C = 15
    OBSERVATION_18_K1_C = 16
    OBSERVATION_18_K2_C = 17
    OBSERVATION_92_K1_C = 18
    OBSERVATION_92_K2_C = 19


class GshH:
    GSH_H_6_K1 = 46
    GSH_H_6_K2 = 47
    GSH_H_18_K1 = 48
    GSH_H_18_K2 = 49
    GSH_H_92_K1 = 50
    GSH_H_92_K2 = 51


class GshB:
    GSH_B_6_K1 = 52
    GSH_B_6_K2 = 53
    GSH_B_18_K1 = 54
    GSH_B_18_K2 = 55
    GSH_B_92_K1 = 56
    GSH_B_92_K2 = 57


class READER:

    def __init__(self, file):
        self.TIME = {}
        self.OBSERVATION = {}
        self.GSH_H = {}
        self.GSH_B = {}

        f = self.__read(file)
        self.file = self.__prepare_file(f)

    @staticmethod
    def __read(file_name):
        return open(file_name).read()

    @staticmethod
    def __prepare_file(file):
        f = file.split('\n')[15:-1]

        new_file = []
        for line in f:

            new_file.append(
                line.split()
            )
        return new_file

    def __get_column(self, number):
        array = []

        translate = int if number == 0 else float

        for row in self.file:
            array.append(
                translate(row[number])
            )

        return array

    def parse(self):
        self.TIME[TIME.T] = {'array': self.__get_column(TIME.T - 1)}

        self.OBSERVATION[ANALOG.OBSERVATION_6_K1_A] = {'array': self.__get_column(ANALOG.OBSERVATION_6_K1_A - 1)}
        self.OBSERVATION[ANALOG.OBSERVATION_6_K2_A] = {'array': self.__get_column(ANALOG.OBSERVATION_6_K2_A - 1)}
        self.OBSERVATION[ANALOG.OBSERVATION_18_K1_A] = {'array': self.__get_column(ANALOG.OBSERVATION_18_K1_A - 1)}
        self.OBSERVATION[ANALOG.OBSERVATION_18_K2_A] = {'array': self.__get_column(ANALOG.OBSERVATION_18_K2_A - 1)}
        self.OBSERVATION[ANALOG.OBSERVATION_92_K1_A] = {'array': self.__get_column(ANALOG.OBSERVATION_92_K1_A - 1)}
        self.OBSERVATION[ANALOG.OBSERVATION_92_K2_A] = {'array': self.__get_column(ANALOG.OBSERVATION_92_K2_A - 1)}

        self.OBSERVATION[DIGITAL.OBSERVATION_6_K1_C] = {'array': self.__get_column(DIGITAL.OBSERVATION_6_K1_C - 1)}
        self.OBSERVATION[DIGITAL.OBSERVATION_6_K2_C] = {'array': self.__get_column(DIGITAL.OBSERVATION_6_K2_C - 1)}
        self.OBSERVATION[DIGITAL.OBSERVATION_18_K1_C] = {'array': self.__get_column(DIGITAL.OBSERVATION_18_K1_C - 1)}
        self.OBSERVATION[DIGITAL.OBSERVATION_18_K2_C] = {'array': self.__get_column(DIGITAL.OBSERVATION_18_K2_C - 1)}
        self.OBSERVATION[DIGITAL.OBSERVATION_92_K1_C] = {'array': self.__get_column(DIGITAL.OBSERVATION_92_K1_C - 1)}
        self.OBSERVATION[DIGITAL.OBSERVATION_92_K2_C] = {'array': self.__get_column(DIGITAL.OBSERVATION_92_K2_C - 1)}

        self.GSH_B[GshB.GSH_B_6_K1] = {'array': self.__get_column(GshB.GSH_B_6_K1 - 1)}
        self.GSH_B[GshB.GSH_B_6_K2] = {'array': self.__get_column(GshB.GSH_B_6_K2 - 1)}
        self.GSH_B[GshB.GSH_B_18_K1] = {'array': self.__get_column(GshB.GSH_B_18_K1 - 1)}
        self.GSH_B[GshB.GSH_B_18_K2] = {'array': self.__get_column(GshB.GSH_B_18_K2 - 1)}
        self.GSH_B[GshB.GSH_B_92_K1] = {'array': self.__get_column(GshB.GSH_B_92_K1 - 1)}
        self.GSH_B[GshB.GSH_B_92_K2] = {'array': self.__get_column(GshB.GSH_B_92_K2 - 1)}

        self.GSH_H[GshH.GSH_H_6_K1] = {'array':  self.__get_column(GshH.GSH_H_6_K1 - 1)}
        self.GSH_H[GshH.GSH_H_6_K2] = {'array': self.__get_column(GshH.GSH_H_6_K2 - 1)}
        self.GSH_H[GshH.GSH_H_18_K1] = {'array': self.__get_column(GshH.GSH_H_18_K1 - 1)}
        self.GSH_H[GshH.GSH_H_18_K2] = {'array': self.__get_column(GshH.GSH_H_18_K2 - 1)}
        self.GSH_H[GshH.GSH_H_92_K1] = {'array': self.__get_column(GshH.GSH_H_92_K1 - 1)}
        self.GSH_H[GshH.GSH_H_92_K2] = {'array': self.__get_column(GshH.GSH_H_92_K2 - 1)}

    # def __load_Gsh_H(self):
    #     gsh_H = GshH.__dict__
    #
    #     for value in gsh_H:
    #         number = gsh_H[value]
    #
    #         self.GSH_H[number] = {
    #             'array': self.__get_column(number - 1)
    #         }

    def interpret_gsh(self, gshB_or_gshH):
        for value in gshB_or_gshH:
            gsh = gshB_or_gshH[value]
            gsh['interpret'] = {}
            array = gsh['array']

            interpreter = INTERPRETER(array)
            new_array = interpreter.get_interpreted_array()  # получаем интерпретированный массив
            marks = interpreter.get_marks(new_array)  # получаем данные по массиву, где начинаются ГША
            count_on_interval = interpreter.count_on_interval(new_array)  # количество ГША на этом участке

            gsh['interpret']['new_array'] = new_array
            gsh['interpret']['marks'] = marks
            gsh['interpret']['count_on_interval'] = count_on_interval

    def cut_observation(self):
        self.interpret_gsh(self.GSH_B)
        self.interpret_gsh(self.GSH_H)

        for v in self.GSH_H:
            logger.info('%s - %s' % (v, self.GSH_H[v]['interpret']['marks']))

        for v in self.GSH_B:
            logger.info('%s - %s' % (v, self.GSH_B[v]['interpret']['marks']))

        end = self.end_search()
        begin = self.begin_search()

        logger.info('начало - %s и конец - %s предполагаемого наблюдения' % (begin, end))

        end = end + 100
        begin = begin - 100

        logger.info('начало - %s и конец - %s предполагаемого наблюдения (увеличенное окно)' % (begin, end))

        for v in self.GSH_H:
            self.GSH_H[v]['cut_array'] = self.GSH_H[v]['interpret']['new_array'][begin:end]

        for v in self.GSH_B:
            self.GSH_B[v]['cut_array'] = self.GSH_B[v]['interpret']['new_array'][begin:end]

        for v in self.OBSERVATION:
            self.OBSERVATION[v]['cut_array'] = self.OBSERVATION[v]['array'][begin:end]

        for v in self.TIME:
            self.TIME[v]['cut_array'] = self.TIME[v]['array'][begin:end]

    def get_array(self, column):
        for value in self.__dict__:
            if column not in self.__dict__[value]:
                continue

            return self.__dict__[value][column]['cut_array']

    def get_original_array(self, column):
        for value in self.__dict__:
            if column not in self.__dict__[value]:
                continue

            return self.__dict__[value][column]['array']

    def end_search(self):
        new_end = None
        number = None

        all_gsh = {}
        all_gsh.update(self.GSH_H)
        all_gsh.update(self.GSH_B)

        for num in all_gsh:
            gsh = all_gsh[num]['interpret']
            count = gsh['count_on_interval']

            if count != 2:
                continue

            end = gsh['marks'][1]['end']

            if new_end is None:
                new_end = end
                number = num
            elif end > new_end:
                new_end = end
                number = num

        logger.debug(u'Номер столбца у которого gsha позже всех - %s' % number)
        return new_end

    def begin_search(self):
        new_begin = None
        number = None

        all_gsh = {}
        all_gsh.update(self.GSH_H)
        all_gsh.update(self.GSH_B)

        for num in all_gsh:
            gsh = all_gsh[num]['interpret']
            count = gsh['count_on_interval']

            if count != 2:
                continue

            begin = gsh['marks'][0]['begin']

            if new_begin is None:
                new_begin = begin
                number = num
            elif begin < new_begin:
                new_begin = begin
                number = num

        logger.info(u'Номер столбца у которого gsha начинается раньше всех - %s' % number)
        return new_begin


class INTERPRETER:
    ON = 1
    OFF = 0

    def __init__(self, array):
        self.array = array

    @staticmethod
    def count_elements(array):
        elem = {}
        for value in array:
            if value in elem:
                elem[value] += 1
            else:
                elem[value] = 0
        return elem

    @staticmethod
    def __get_percent(x, count):
        return 100 * x / count

    def __repr__(self):
        s = ''
        elem = self.count_elements(self.array)
        count = self.__get_count()

        for value in elem:
            s += 'Значение - %s : %s\n' % (value, self.__get_percent(elem[value], count))
        return s

    def __get_conformity(self, elem):
        conformity = {}
        count = len(self.array)
        for value in elem:
            percent = self.__get_percent(
                elem[value], count
            )
            if percent > 90:
                self.OFF = value
            else:
                self.ON = value
        return conformity

    def __get_count(self):
        return len(self.array)

    @staticmethod
    def count_on_interval(array):  # подсчет непрерывных единичных интервалов
        flag = False
        count = 0
        for num in range(0, len(array)):
            #print(num, array[num])
            if array[num] == 1:
                if not flag:
                    count += 1
                    flag = True
            elif array[num] == 0:
                flag = False
        return count

    def get_interpreted_array(self):
        count = self.__get_count()
        elem = self.count_elements(self.array)
        if len(elem) > 2:
            raise Exception('Элементов в массиве больше двух!')
        self.__get_conformity(elem)

        interpreted_array = self.__interpret(count, self.array)
        logger.info('Массив интепретированный %s' % interpreted_array)

        interpreted_array = self.filter(interpreted_array)
        logger.info('Массив отфлитрованный %s' % interpreted_array)

        logger.info('Непрерывных интервалов = %s' % self.count_on_interval(interpreted_array))

        return interpreted_array

    def __interpret(self, count, array):
        interpreted_array = copy.deepcopy(array)
        for num in range(0, count):
            elem = array[num]
            if elem == self.ON:
                interpreted_array[num] = 1
            elif elem == self.OFF:
                interpreted_array[num] = 0
        return interpreted_array

    def get_marks(self, array):
        flag = False
        marks = []
        mark = {}
        for num, val in enumerate(array):
            if val == 1 and not flag:
                mark = {'begin': num}
                flag = True
            elif val == 0 and flag:
                mark['end'] = num
                flag = False
                mark['count'] = mark['end'] - mark['begin']
                marks.append(mark)

        if flag:  # если последний элемент == 1
            mark['end'] = self.__get_count()
            mark['count'] = mark['end'] - mark['begin']
            marks.append(mark)
        return marks

    @staticmethod
    def __remake(value, begin, end, massive):
        for num in range(begin, end):
            massive[num] = value

    def filter(self, array):
        marks = self.get_marks(array)  # получить массив с отметками где начинаются единички и заканчиваются
        logger.debug(marks)
        self.__first_filter(array, marks)  # фильтр для интервалов с длиной 1, 2
        logger.debug(array)

        marks = self.get_marks(array)
        logger.debug(marks)

        self.__second_filter(array, marks)  # фильр для длинных интервалов, которые отличаются от всех остальных
        logger.debug(array)

        try:
            for num, value in enumerate(marks):
                end = value['end']
                begin = marks[num + 1]['begin']
                print('Between %s - %s. Way - %s' % (num, num + 1, begin - end))
        except Exception as e:
            print(e)
            print('exit')

        return array

    def __first_filter(self, array, marks):
        for mark in marks:
            begin = mark['begin']
            end = mark['end']

            if end - begin in [1, 2, 3, 4, 5]:  # интервалы с длинами 1, 2, 3, 4, 5 - фильтруются
                self.__remake(0, begin, end, array)

    def __second_filter(self, array, marks):
        elements = self.__get_excess_elements(marks)
        logger.debug('Лишние элементы %s' % elements)

        for element in elements:
            begin = element['begin']
            end = element['end']

            self.__remake(0, begin, end, array)

    def __get_excess_elements(self, marks):
        for num, value in enumerate(marks):
            value['comparisons'] = self.__get_comparisons(num, value, marks)  # получить сравнение со всеми эелементами в marks
        logger.debug('Marks с массивом сравнений %s' % marks)

        excess_elements = []
        for num, val in enumerate(marks):
            comparisons = val['comparisons']
            if comparisons != [] and self.__is_superfluous_expression(comparisons):
                excess_elements.append(marks[num])
        return excess_elements

    @staticmethod
    def __is_superfluous_expression(comparisons):
        excess = True

        for value in comparisons:
            if value < 10:
                excess = False

        return excess

    def __get_comparisons(self, number, mark, marks):
        comparisons = []
        count = mark['begin'] - mark['end']
        for num, elem in enumerate(marks):
            elem_count = elem['begin'] - elem['end']
            percent = abs(100 - self.__get_percent(count, elem_count))
            if num != number:
                comparisons.append(percent)
        return comparisons



if __name__ == '__main__':
    # array = [1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1]
    # interpret = INTERPRETER(array)
    # print(interpret.filter(array))
    # a = {1:2, 3:4}
    # for i in a:
    #     print(a[i])
    #
    #
    # exit()
    import matplotlib.pyplot as plt
    from src.log import setup_logger
    setup_logger()
    file = 'out_6_92cm_spectr_20180110_133129_02_04_nomer_2.tmi'
    file2 = 'out_6_92cm_spectr_20180110_133129_02_04_nomer_2.tmi'
    file3 = 'out_6_92cm_spectr_20180124_004919_01_05_nomer_1.tmi'
    file4 = 'out_6_92cm_spectr_20180212_180710_02_02_nomer_3.tmi'
    file5 = 'out_6_92cm_spectr_20180228_165341_01_02_nomer_4.tmi'
    file6 = 'out_6_92cm_spectr_20180309_161910_02_02.tmi'
    file7 = 'out_6_92cm_spectr_20180309_161910_02_02_nomer_5.tmi'
    reader = READER(file7)
    reader.parse()

    reader.cut_observation()

    for i in reader.OBSERVATION:
        x = reader.get_original_array(TIME.T)
        y = reader.get_original_array(i)

        # plt.scatter(t, y, s=5) #i.get_interpreted_array(), s=5)
        plt.scatter(x, y, s=5)
        plt.xlabel(r'$x$')
        plt.ylabel(r'$f(y)$')
        plt.title(r'$y=$')
        plt.grid(True)
        plt.show()

        x = reader.get_array(TIME.T)
        y = reader.get_array(i)

        #plt.scatter(t, y, s=5) #i.get_interpreted_array(), s=5)
        plt.scatter(x, y, s=5)
        plt.xlabel(r'$x$')
        plt.ylabel(r'$f(y)$')
        plt.title(r'$y=$')
        plt.grid(True)
        plt.show()
