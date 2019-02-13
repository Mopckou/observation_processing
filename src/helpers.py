import copy
import numpy
import scipy
import random
import logging

logger = logging.getLogger('LOG')


class TIME:
    T = 1


class ANALOG:
    OBSERVATION_6_K1 = 6
    OBSERVATION_6_K2 = 7
    OBSERVATION_18_K1 = 8
    OBSERVATION_18_K2 = 9
    OBSERVATION_92_K1 = 10
    OBSERVATION_92_K2 = 11


class DIGITAL:
    OBSERVATION_6_K1 = 14
    OBSERVATION_6_K2 = 15
    OBSERVATION_18_K1 = 16
    OBSERVATION_18_K2 = 17
    OBSERVATION_92_K1 = 18
    OBSERVATION_92_K2 = 19


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

        self.OBSERVATION[ANALOG.OBSERVATION_6_K1] = {'array': self.__get_column(ANALOG.OBSERVATION_6_K1 - 1)}
        self.OBSERVATION[ANALOG.OBSERVATION_6_K2] = {'array': self.__get_column(ANALOG.OBSERVATION_6_K2 - 1)}
        self.OBSERVATION[ANALOG.OBSERVATION_18_K1] = {'array': self.__get_column(ANALOG.OBSERVATION_18_K1 - 1)}
        self.OBSERVATION[ANALOG.OBSERVATION_18_K2] = {'array': self.__get_column(ANALOG.OBSERVATION_18_K2 - 1)}
        self.OBSERVATION[ANALOG.OBSERVATION_92_K1] = {'array': self.__get_column(ANALOG.OBSERVATION_92_K1 - 1)}
        self.OBSERVATION[ANALOG.OBSERVATION_92_K2] = {'array': self.__get_column(ANALOG.OBSERVATION_92_K2 - 1)}

        self.OBSERVATION[DIGITAL.OBSERVATION_6_K1] = {'array': self.__get_column(DIGITAL.OBSERVATION_6_K1 - 1)}
        self.OBSERVATION[DIGITAL.OBSERVATION_6_K2] = {'array': self.__get_column(DIGITAL.OBSERVATION_6_K2 - 1)}
        self.OBSERVATION[DIGITAL.OBSERVATION_18_K1] = {'array': self.__get_column(DIGITAL.OBSERVATION_18_K1 - 1)}
        self.OBSERVATION[DIGITAL.OBSERVATION_18_K2] = {'array': self.__get_column(DIGITAL.OBSERVATION_18_K2 - 1)}
        self.OBSERVATION[DIGITAL.OBSERVATION_92_K1] = {'array': self.__get_column(DIGITAL.OBSERVATION_92_K1 - 1)}
        self.OBSERVATION[DIGITAL.OBSERVATION_92_K2] = {'array': self.__get_column(DIGITAL.OBSERVATION_92_K2 - 1)}

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
            logger.info('Обработка ГША - %s' % value)
            gsh = gshB_or_gshH[value]
            gsh['interpret'] = {}
            array = gsh['array']

            interpreter = INTERPRETER(array)
            new_array = interpreter.get_interpreted_array()  # получаем интерпретированный массив
            marks = interpreter.get_single_intervals(new_array)  # получаем данные по массиву, где начинаются ГША
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
            self.GSH_H[v]['current_array'] = self.GSH_H[v]['cut_array']

        for v in self.GSH_B:
            self.GSH_B[v]['cut_array'] = self.GSH_B[v]['interpret']['new_array'][begin:end]
            self.GSH_B[v]['current_array'] = self.GSH_B[v]['cut_array']

        for v in self.OBSERVATION:
            self.OBSERVATION[v]['cut_array'] = self.OBSERVATION[v]['array'][begin:end]
            self.OBSERVATION[v]['current_array'] = self.OBSERVATION[v]['cut_array']

        for v in self.TIME:
            self.TIME[v]['cut_array'] = self.TIME[v]['array'][begin:end]
            self.TIME[v]['current_array'] = self.TIME[v]['cut_array']  # делаем ссылку на корректный объект, который
            # вызывается  методом get_array

    def get_array(self, column):
        for value in self.__dict__:
            if column not in self.__dict__[value]:
                continue

            return self.__dict__[value][column]['current_array']

    def get_original_array(self, column):
        for value in self.__dict__:
            if column not in self.__dict__[value]:
                continue

            return self.__dict__[value][column]['array']

    def end_search(self):
        end_search_gsh_h, number_gsh_h = self.__end_search(self.GSH_H)
        end_search_gsh_b, number_gsh_b = self.__end_search(self.GSH_B)

        if end_search_gsh_b > end_search_gsh_h:
            logger.debug(u'Номер столбца у которого gsha позже всех - %s' % number_gsh_b)
            return end_search_gsh_b

        logger.debug(u'Номер столбца у которого gsha позже всех - %s' % number_gsh_h)
        return end_search_gsh_h

    def __end_search(self, gsha):
        new_end = None
        number = None

        for num in gsha:
            gsh = gsha[num]['interpret']
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

        return new_end, number

    def begin_search(self):
        begin_gsh_h, number_gsh_h = self.__begin_search(self.GSH_H)
        begin_gsh_b, number_gsh_b = self.__begin_search(self.GSH_B)

        if begin_gsh_b < begin_gsh_h:
            logger.debug(u'Номер столбца у которого gsha начинается раньше всех - %s' % number_gsh_b)
            return begin_gsh_b

        logger.debug(u'Номер столбца у которого gsha начинается раньше всех - %s' % number_gsh_h)
        return begin_gsh_h

    def __begin_search(self, gsha):
        new_begin = None
        number = None

        for num in gsha:
            gsh = gsha[num]['interpret']
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

        return new_begin, number

    @staticmethod
    def filter_by_etalon(etalon_erray, array, delta):
        last_correct_value = None
        new_array = []

        for num, etalon_value in enumerate(etalon_erray):
            array_value = array[num]
            #if array_value == 0:
                #new_array.append(random.uniform(last_correct_value - 0.01, last_correct_value + 0.01))
            if READER.__in(etalon_value, array_value, delta):
                new_array.append(array_value)
                last_correct_value = array_value
            elif last_correct_value is None:  # если в цифре с самого начала зашкаальные значения
                new_array.append(etalon_value)
            else:
                new_array.append(etalon_value)
        return new_array

    def filter_digital_observation(self):
        """
        Функция корректирует цифровые наблюдения (заменяет ошибочные значения) на основе аналогового наблюдения.
        Т.к. в аналоговых наблюдениях ошибочных значений нет.
        :return: 
        """
        delta = {
            DIGITAL.OBSERVATION_6_K1: 0.2,
            DIGITAL.OBSERVATION_6_K2: 0.2,
            DIGITAL.OBSERVATION_18_K1: 0.6,
            DIGITAL.OBSERVATION_18_K2: 0.6,
            DIGITAL.OBSERVATION_92_K1: 0.05,
            DIGITAL.OBSERVATION_92_K2: 0.05
        }

        for value in self.OBSERVATION:

            if value not in DIGITAL.__dict__.values():
                continue

            key = self.__get_key_name(DIGITAL.__dict__, value)
            logger.info('Обрабатывается наблюдение - %s' % key)
            logger.debug('Value - %s, Key - %s, Delta - %s' % (value, key, delta[value]))

            array = self.filter_by_etalon(
                self.get_array(ANALOG.__dict__[key]),
                self.get_array(DIGITAL.__dict__[key]),
                delta[value]
            )
            logger.debug('Новый отфильтрованный массив: %s' % array)

            self.OBSERVATION[value]['filtered_array'] = array
            self.OBSERVATION[value]['current_array'] = self.OBSERVATION[value]['filtered_array']  # меняем ссылку на
            # возвращаемый массив в get_array

    def trim_to_seconds(self):
        """
        Функция обрезает файлы наблюдений до секунд.
        :return: 
        """
        array_with_sec = self.__array_to_seconds(
            self.get_array(TIME.T)
        )
        tags = self.__get_trim_tags(array_with_sec)

        for v in self.GSH_H:
            self.GSH_H[v]['trim_array'] = self.__trim_by_tags(self.get_array(v), tags)
            self.GSH_H[v]['current_array'] = self.GSH_H[v]['trim_array']

        for v in self.GSH_B:
            self.GSH_B[v]['trim_array'] = self.__trim_by_tags(self.get_array(v), tags)
            self.GSH_B[v]['current_array'] = self.GSH_B[v]['trim_array']

        for v in self.OBSERVATION:
            self.OBSERVATION[v]['trim_array'] = self.__trim_by_tags(self.get_array(v), tags)
            self.OBSERVATION[v]['current_array'] = self.OBSERVATION[v]['trim_array']

        for v in self.TIME:
            self.TIME[v]['trim_array'] = self.__trim_by_tags(array_with_sec, tags)
            self.TIME[v]['current_array'] = self.TIME[v]['trim_array']

    def trim_bad_areas(self):
        areas = self.__find_bad_areas()  # найти не корректные участки, которые обычно = 0.
        tags = self.__convert_areas_to_array_tags(
            self.get_array(TIME.T), areas
        )

        for v in self.GSH_H:
            self.GSH_H[v]['recovered_array'] = self.__trim_by_tags(self.get_array(v), tags)
            self.GSH_H[v]['current_array'] = self.GSH_H[v]['recovered_array']

        for v in self.GSH_B:
            self.GSH_B[v]['recovered_array'] = self.__trim_by_tags(self.get_array(v), tags)
            self.GSH_B[v]['current_array'] = self.GSH_B[v]['recovered_array']

        for v in self.OBSERVATION:
            self.OBSERVATION[v]['recovered_array'] = self.__trim_by_tags(self.get_array(v), tags)
            self.OBSERVATION[v]['current_array'] = self.OBSERVATION[v]['recovered_array']

        for v in self.TIME:
            self.TIME[v]['recovered_array'] = self.__adjust_time_array(self.get_array(v), tags)
            self.TIME[v]['current_array'] = self.TIME[v]['recovered_array']  # делаем ссылку на корректный объект, который
            # вызывается  методом get_array

    def __adjust_time_array(self, array, tags):
        recovered_array = self.__trim_by_tags(array, tags)
        count = len(recovered_array)

        return array[:count]

    @staticmethod
    def meaningful_data(array):
        acceptable_minimum = 0.1
        dispersion = numpy.var(array, ddof=1)

        return dispersion > acceptable_minimum

    def __find_bad_areas(self):
        areas_by_observation = {}

        for value in self.OBSERVATION:  # цикл по всем цифровым наблюдениям

            if value not in DIGITAL.__dict__.values():  # ищем иммено цифровое наблюдение
                continue

            key = self.__get_key_name(DIGITAL.__dict__, value)  # получаем имя наблюдения, например: OBSERVATION_6_K1
            logger.info('Обрабатывается наблюдение - %s' % key)
            logger.debug('Value - %s, Key - %s' % (value, key))

            digital_array = self.get_array(DIGITAL.__dict__[key])
            analog_array = self.get_array(ANALOG.__dict__[key])

            if not self.meaningful_data(digital_array) or not self.meaningful_data(analog_array):
                continue

            digital_intervals = INTERPRETER.get_equal_intervals(digital_array)
            logger.debug('Одинаковые интервалы у цифры: %s' % digital_intervals)

            analog_intervals = INTERPRETER.get_equal_intervals(analog_array)
            logger.debug('Одинаковые интервалы у аналога: %s' % analog_intervals)

            identical_intervals = self.__get_identical_intervals(analog_intervals, digital_intervals, key, True)
            logger.debug('Идентичные интервалы у аналогового и цифрового наблюдения: %s' % identical_intervals)

            areas_by_observation[key] = identical_intervals

        return self.__find_equal_areas_by_observations(areas_by_observation)

    def __find_equal_areas_by_observations(self, areas_by_observations):
        founded_intervals = []

        for observation in areas_by_observations:
            for other_observation in areas_by_observations:

                if observation == other_observation:
                    continue

                area = areas_by_observations[observation]
                other_area = areas_by_observations[other_observation]

                identical_intervals = self.__get_identical_intervals(area, other_area)

                founded_intervals = self.__update(founded_intervals, identical_intervals)
        for i in founded_intervals:
            print(i)
        logger.debug('Интервалы для удаления: %s' % founded_intervals)
        return founded_intervals

    def __update(self, massive, array):

        for value in array:
            if not self.__area_is_exists(massive, value):
                massive.append(value)

        return massive

    def __area_is_exists(self, massive, area):
        for other_area in massive:
            if self.__interval_is_identical(area, other_area):
                return True
        return False

    @staticmethod
    def __trim_by_tags(array, tag_array):
        new_array = []

        for num, val in enumerate(array):
            if tag_array[num]:
                new_array.append(val)

        return new_array

    @staticmethod
    def __get_trim_tags(array):
        new_array = []
        before_value = None

        for num, value in enumerate(array):
            if value != before_value:
                new_array.append(True)
                before_value = value
            else:
                new_array.append(False)

        return new_array

    def __convert_areas_to_array_tags(self, array, areas):
        tags = [True for i in array]

        for area in areas:
            begin = area['begin']
            end = area['end']
            tags = self.__mark_an_area(begin, end, tags)

        return tags

    @staticmethod
    def __mark_an_area(begin, end, tags):
        for i in range(begin, end + 1):
            tags[i] = False

        return tags

    @staticmethod
    def __array_to_seconds(array):
        new_array = copy.deepcopy(array)

        for num, value in enumerate(new_array):
            value = int(value) / 1000
            new_array[num] = int(value)
        return new_array

    @staticmethod
    def __in(etalon_value, value, delta):
        return value < etalon_value + delta and etalon_value - delta < value

    @staticmethod
    def __get_key_name(from_dict, needed_value):
        for key, value in from_dict.items():
            if value == needed_value:
                return key

    def get_name_observation(self, column):
        key = self.__get_key_name(DIGITAL.__dict__, column)

        if key is not None:
            return key

        key = self.__get_key_name(ANALOG.__dict__, column)

        if key is not None:
            return key

    def __get_identical_intervals(self, intervals, other_intervals, key=None, flag=False):
        identical_intervals = []

        for interval in intervals:
            for other_interval in other_intervals:

                if self.__interval_is_identical(interval, other_interval):
                    if flag:
                        other_interval['observation'] = key
                    identical_intervals.append(other_interval)

        return identical_intervals

    @staticmethod
    def __interval_is_identical(interval, other_interval):
        return interval['begin'] == other_interval['begin'] and interval['end'] == other_interval['end']


class WRITER:

    def __init__(self, file_name):
        self.__file = file_name

    def write_result(self):
        pass


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

    @staticmethod
    def get_average(array):
        #summary = 0.

        # for elem in array:
        #     summary += elem
        return sum(array) / len(array)

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

    @staticmethod
    def get_single_intervals(array):
        flag = False
        marks = []
        mark = {}
        for num, val in enumerate(array):
            if float(val) == 1. and not flag:
                mark = {'begin': num}
                flag = True
            elif float(val) == 0. and flag:
                mark['end'] = num
                flag = False
                mark['count'] = mark['end'] - mark['begin']
                marks.append(mark)

        if flag:  # если последний элемент == 1
            mark['end'] = len(array)
            mark['count'] = mark['end'] - mark['begin']
            marks.append(mark)
        return marks

    @staticmethod
    def get_zero_intervals(array):
        flag = False
        marks = []
        mark = {}
        for num, val in enumerate(array):
            if val == 0 and not flag:
                mark = {'begin': num}
                flag = True
            elif val != 0 and flag:
                mark['end'] = num
                flag = False
                mark['count'] = mark['end'] - mark['begin']
                marks.append(mark)

        if flag:  # если последний элемент == 1
            mark['end'] = len(array)
            mark['count'] = mark['end'] - mark['begin']
            marks.append(mark)
        return marks

    @staticmethod
    def get_equal_intervals(array):
        """
        Метод возвращает непрерывные интервалы массива, которые имеют одинаковое значение внутри одного интервала.
        :param array: 
        :return: 
        """
        flag = False
        marks = []
        mark = {}
        for num, val in enumerate(array[:-1]):
            if val == array[num + 1] and not flag:
                mark = {
                    'value': val,
                    'begin': num
                }
                flag = True
            elif val == array[num + 1] and flag:
                pass
            elif val != array[num + 1] and flag:
                mark['end'] = num
                flag = False
                mark['count'] = mark['end'] - mark['begin'] + 1  # колличество одинаковых точек (+1 т.к. включительно)
                marks.append(mark)

        if flag:  # если последний элемент == 1
            mark['end'] = len(array) - 1
            mark['count'] = mark['end'] - mark['begin'] + 1
            marks.append(mark)
        return marks

    @staticmethod
    def __remake(value, begin, end, massive):
        for num in range(begin, end):
            massive[num] = value

    def filter(self, array):
        marks = self.get_single_intervals(array)  # получить массив с отметками где начинаются единички и заканчиваются
        logger.debug(marks)
        self.__first_filter(array, marks)  # фильтр для интервалов с длиной 1, 2
        logger.debug(array)

        marks = self.get_single_intervals(array)
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
            if value < 25:
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
    a = [50, 51, 52, 44, 61, 100, 54, 49, 46, 57, 59]
    print(sum(a)/len(a))
    print(numpy.var(a, ddof=1))
    # array = [1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1]
    # interpret = INTERPRETER(array)
    # print(interpret.filter(array))
    # a = {1:2, 3:4}
    # # for i in a:
    # #     print(a[i])
    # #
    # #
    # # exit()
    # import matplotlib.pyplot as plt
    #
    # def plot(abscissa, ordinate):
    #     x = abscissa
    #     y = ordinate
    #     plt.scatter(x, y, s=5)
    #     plt.xlabel(r'$x$')
    #     plt.ylabel(r'$f(y)$')
    #     plt.title(r'$y=$')
    #     plt.grid(True)
    #     plt.show()
    #
    # from src.log import setup_logger
    # from src.finder_gsh import FinderGsh
    # setup_logger()
    # file = 'out_6_92cm_spectr_20180110_133129_02_04_nomer_2.tmi'
    # file4 = 'out_6_92cm_spectr_20180212_180710_02_02_nomer_3.tmi'
    # file5 = 'out_6_92cm_spectr_20180228_165341_01_02_nomer_4.tmi'  # готов
    # file6 = 'out_6_92cm_spectr_20180309_161910_02_02.tmi'
    # reader = READER(file4)
    # reader.parse()
    #
    # reader.cut_observation()
    # reader.filter_digital_observation()
    # reader.trim_to_seconds()
    # reader.trim_bad_areas()
    # # import numpy
    # #
    # # print(numpy.var(reader.get_array(DIGITAL.OBSERVATION_6_K1), ddof=1))
    # # print(numpy.var(reader.get_array(DIGITAL.OBSERVATION_6_K2), ddof=1))
    # # print(numpy.var(reader.get_array(DIGITAL.OBSERVATION_18_K1), ddof=1))
    # # print(numpy.var(reader.get_array(DIGITAL.OBSERVATION_18_K2), ddof=1))
    # # print(numpy.var(reader.get_array(DIGITAL.OBSERVATION_92_K1), ddof=1))
    # # print(numpy.var(reader.get_array(DIGITAL.OBSERVATION_92_K2), ddof=1))
    # # input()
    # # exit()
    #
    # # parser = GshParser()
    # # parser.indent = 4
    # # parser.set_ordinate(reader.get_array(ANALOG.OBSERVATION_18_K1_A))
    # # parser.set_abscissa(reader.get_array(TIME.T))
    # #
    # # parser.set_gsh_B(GshB.GSH_B_18_K1, 1, reader.get_array(GshB.GSH_B_18_K1))
    # # parser.set_gsh_B(GshB.GSH_B_18_K2, 2, reader.get_array(GshB.GSH_B_18_K2))
    # #
    # # parser.set_gsh_H(GshH.GSH_H_18_K1, 1, reader.get_array(GshH.GSH_H_18_K1))
    # # parser.set_gsh_H(GshH.GSH_H_18_K2, 2, reader.get_array(GshH.GSH_H_18_K2))
    # #
    # # parser.find_gauss()
    # # print(parser.get_description())
    # # print(parser.get_result())
    # # print(parser.report)
    # # parser.build_graph()
    # operator = OPERATOR()
    # operator.set_reader(reader)
    # operator.find_gsh(DIGITAL.OBSERVATION_6_K1)
    # operator.find_gsh(DIGITAL.OBSERVATION_6_K2)
    #
    # operator.find_gsh(DIGITAL.OBSERVATION_18_K1)
    # operator.find_gsh(DIGITAL.OBSERVATION_18_K2)
    # #plot(reader.get_array(TIME.T), reader.get_array(ANALOG.OBSERVATION_92_K1))
    #
    # operator.find_gsh(DIGITAL.OBSERVATION_92_K1)
    # #plot(reader.get_array(TIME.T), reader.get_array(ANALOG.OBSERVATION_92_K2))
    #
    # operator.find_gsh(DIGITAL.OBSERVATION_92_K2)
    # exit()
