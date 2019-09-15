import os
import copy
import numpy
import scipy
import random
import errno
import logging

logger = logging.getLogger('LOG')

LOG_DIRECTORY = os.path.join(os.getcwd(), 'OUT')


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


OBSERVATIONS = [
    DIGITAL.OBSERVATION_6_K1,
    DIGITAL.OBSERVATION_6_K2,
    DIGITAL.OBSERVATION_18_K1,
    DIGITAL.OBSERVATION_18_K2,
    DIGITAL.OBSERVATION_92_K1,
    DIGITAL.OBSERVATION_92_K2,
]


SETUP = {
    DIGITAL.OBSERVATION_6_K1: (1, 25, 80, 0.3),
    DIGITAL.OBSERVATION_6_K2: (1, 25, 80, 0.3),
    DIGITAL.OBSERVATION_18_K1: (1, 100, 140, 0.8),
    DIGITAL.OBSERVATION_18_K2: (1, 100, 140, 0.8),
    DIGITAL.OBSERVATION_92_K1: (80, 150, 320, 0.8),
    DIGITAL.OBSERVATION_92_K2: (80, 150, 320, 0.8)
}


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

GROUPS = {
    'OBSERVATION_6': [
        DIGITAL.OBSERVATION_6_K1,
        DIGITAL.OBSERVATION_6_K2,
        ANALOG.OBSERVATION_6_K1,
        ANALOG.OBSERVATION_6_K2
    ],
    'OBSERVATION_18': [
        DIGITAL.OBSERVATION_18_K1,
        DIGITAL.OBSERVATION_18_K2,
        ANALOG.OBSERVATION_18_K1,
        ANALOG.OBSERVATION_18_K2
    ],
    'OBSERVATION_92': [
        DIGITAL.OBSERVATION_92_K1,
        DIGITAL.OBSERVATION_92_K2,
        ANALOG.OBSERVATION_92_K1,
        ANALOG.OBSERVATION_92_K2
    ],
}

class READER:

    def __init__(self, file):
        self.TIME = {}
        self.OBSERVATION = {}
        self.GSH_H = {}
        self.GSH_B = {}

        f = self.__read(file)
        self.file = self.__prepare_file(f)
        self.plots = []

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

    def get_file(self):
        return self.file

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
            marks = interpreter.get_single_intervals(new_array)  # получаем данные по массиву, где начинаются ГШ
            count_on_interval = interpreter.count_on_interval(new_array)  # количество ГШ на этом участке

            gsh['interpret']['new_array'] = new_array
            gsh['interpret']['marks'] = marks
            gsh['interpret']['count_on_interval'] = count_on_interval
            #input()

    def cut_observation(self):
        self.interpret_gsh(self.GSH_B)
        self.interpret_gsh(self.GSH_H)

        for v in self.GSH_H:
            logger.info('%s - %s' % (v, self.GSH_H[v]['interpret']['marks']))

        for v in self.GSH_B:
            logger.info('%s - %s' % (v, self.GSH_B[v]['interpret']['marks']))

        #input()
        begin, end = self.__search_observation(self.GSH_H, self.GSH_B, self.TIME[TIME.T]['array'])
        #exit()

        # end = self.end_search()
        # begin = self.begin_search()

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

    def get_time(self, column):
        if 'time' in self.get_object(column):
            return self.get_object(column)['time']

        return self.get_array(TIME.T)

    def get_array(self, column):
        return self.get_object(column)['current_array']

    def get_object(self, column):
        """
        Получение обьекта по номеру столбца.
        Например получить обьект который содержит 14 столбец. На выхооде будет dict который содержится в
        OBSERVATION[DIGITAL.OBSERVATION_6_K1]

        :param column:
        :return:
        """
        for value in self.__dict__:
            if column not in self.__dict__[value]:
                continue

            return self.__dict__[value][column]

        raise Exception('Наблюдение не найдено!')

    def get_original_array(self, column):
        for value in self.__dict__:
            if column not in self.__dict__[value]:
                continue

            return self.__dict__[value][column]['array']

    def __search_observation(self, nsl, nsh, t):
        ABS_WIDTH = 5  # ширина в процентах относительно файла наблдения. Параметр width не должен быть меньше!
        ABS_PILLAR = 20  # ширина ГША не должа быть меньше чем ABS_PILLAR

        ns = {**nsl, **nsh}
        areas = []
        len_obs = len(t)

        for num in ns:  # собираем все участки в один массив, чтобы потом групировать
            areas.extend(
                self.__transform_mark_to_area(ns[num]['interpret']['marks'], len_obs)
            )

        areas = list(filter(lambda x: x.abs_width > ABS_WIDTH, areas))  # фильтруются предполагаемые наблюдения
        # у которых шиина наблюдения меньше чем ABS_WIDTH
        logger.debug('Фильтруем предполагамые наблюдения у которых ширина меньше допустимного предела: %s' % areas)

        areas = list(filter(lambda x: x.pillar_deviation < ABS_PILLAR, areas))
        logger.debug('Фильтруем предполагаемые наблюдения у которых ширины ГША отклоняются друг от друга: %s' % areas)

        groups = self.break_down_into_groups(areas)  # группируем предполагаемые наблюдения
        logger.debug('Сгруппированные предполагамемые наблюдения: \n%s' %
                     '\n-------------------------\n'.join(self.prepare_for_log(group) for group in groups))

        groups = sorted(groups, key=lambda x: len(x))  # сортриуем группы по количеству в них найденных элементов

        if not groups:
            raise Exception('Не найдено предполагаемое наблюдение!')

        obs_group = groups[-1]
        logger.debug('Найденная группа: \n%s' % self.prepare_for_log(obs_group))

        begin = sorted(obs_group, key=lambda x: x.begin)[0].begin
        end = sorted(obs_group, key=lambda x: x.end)[-1].end

        return begin, end

    @staticmethod
    def prepare_for_log(array):
        return '\n'.join(str(i) for i in array)

    @staticmethod
    def break_down_into_groups(sites):
        groups = []

        for key, val in enumerate(sites):
            res, group = READER.group_attitue_check(val, groups)

            if res:
                group.append(val)
                continue

            if val in sites[key + 1:]:
                groups.append([val])

        return groups

    @staticmethod
    def __transform_mark_to_area(marks, len_obs):
        """
        Преобразование mark в участки (area). Которые представляют собой отрезок от mark1 до mark2
        :param marks: 
        :return: 
        """
        areas = []

        for k, v in enumerate(marks[:-1]):
            first_elem = marks[k]
            second_elem = marks[k + 1]
            #width = second_elem['begin'] - first_elem['begin']
            areas.append(
                Area(first_elem['begin'], second_elem['begin'], first_elem['count'], second_elem['count'], len_obs)
            )

        return areas

    @staticmethod
    def group_attitue_check(site, groups):
        """
        Проверка что участок соответствует одной из групп
        :param site:
        :param groups: 
        :return: 
        """
        for group in groups:
            if site in group:
                return True, group

        return False, None

    # @staticmethod
    # def __get_a_hot_area(_list, value):
    #     begin = _list.index(value)
    #
    #     end = -1
    #     for key in range(begin, len(_list)):
    #         if _list[key] != value:
    #             break
    #
    #         end = key
    #
    #     return begin, end



    # def __increment_area(self, _list, begin, end):
    #     [self.__increment_value(_list, index) for index in range(begin, end)]
    #
    # @staticmethod
    # def __increment_value(_list, index):
    #     _list[index] += 1
    #
    # def __is_location(self, subgroup1, subgroup2):
    #     elem1 = subgroup1[0]
    #     elem2 = subgroup2[0]
    #
    #     count = len(self.TIME[TIME.T]['array'])


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
    def filter_by_etalon(etalon_array, array, delta):
        last_correct_value = None
        new_array = []

        for num, etalon_value in enumerate(etalon_array):
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
            DIGITAL.OBSERVATION_18_K1: 0.3,
            DIGITAL.OBSERVATION_18_K2: 0.3,
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

    def filter_bad_single_values(self):
        pass

    def handle_observation(self, array):

        for num, value in enumerate(array[:-3]):
            first_value = array[num]
            second_value = array[num + 1]
            third_value = array[num + 2]

            aver = INTERPRETER.get_average([first_value, third_value])
            if second_value - aver > 1:
                array[num + 1] = first_value

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
        #areas = self.__delete_equal(areas)
        areas = self.__split_into_group(areas)

        self.trim_bad_areas_in_ns(areas)
        self.trim_bad_areas_in_observations(areas)

    def __split_into_group(self, areas):
        """
        Разделение участков которые нужно удалить на группы:
        1. 6см - (канал 1, канал 2)
        2. 18см - (канал 1, канал 2)
        3. 92см - (канал 1, канал 2)
        """

        groups = {}
        print(areas)
        for group in GROUPS:
            groups[group] = [area for area in areas if group in area['observation']]

        return groups

    def trim_bad_areas_in_ns(self, observation_group):
        # areas = self.__delete_equal_areas(areas)
        # logger.debug('Уникальные интервалы для массива с ГШ: %s' % areas)
        # input()
        for group in observation_group:
            observation_num = GROUPS[group][0]  # берем номер наблюдения с 1 каналом. ГША общий для обоих каналов
            # поэтому можно взять любой и вырезать плохие участки в ГША массиве
            areas = observation_group[group]
            tags = self.__convert_areas_to_array_tags(
                self.get_array(TIME.T), areas
            )

            ns = TABLE[observation_num]  # получение ГШ по номеру наблюдения
            for num in ns.values():
                obj = self.get_object(num)
                obj['recovered_array'] = self.__trim_by_tags(self.get_array(num), tags)
                obj['current_array'] = obj['recovered_array']

    def trim_bad_areas_in_observations(self, observation_group):
        for group_name in observation_group:
            for observation_number in GROUPS[group_name]:
                areas = observation_group[group_name]
                tags = self.__convert_areas_to_array_tags(
                    self.get_array(TIME.T), areas
                )
                observation = self.OBSERVATION[observation_number]

                obs_array = self.get_array(observation_number)
                observation['recovered_array'] = self.__trim_by_tags(obs_array, tags)
                observation['current_array'] = observation['recovered_array']
                observation['time'] = self.__adjust_time_array(self.get_array(TIME.T), tags)

    def trim_bad_areas_old(self):
        areas = self.__find_bad_areas_old()  # найти не корректные участки, которые обычно = 0.
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

    def replace_bad_values(self):
        logger.info('ЗАМЕНА ПЛОХИХ ЗНАЧЕНИЙ!')
        for value in self.OBSERVATION:

            if value not in DIGITAL.__dict__.values():
                continue

            key = self.__get_key_name(DIGITAL.__dict__, value)
            logger.info('Обрабатывается наблюдение - %s' % key)
            logger.debug('Value - %s, Key - %s' % (value, key))

            array = self.__replace_bad_values(
                self.get_array(ANALOG.__dict__[key]),
                self.get_array(DIGITAL.__dict__[key]),
            )
            logger.debug('Новый c замененными значениями: %s' % array)

            self.OBSERVATION[value]['replaced_array'] = array
            self.OBSERVATION[value]['current_array'] = self.OBSERVATION[value]['replaced_array']  # меняем ссылку на
            # возвращаемый массив в get_array

    def __replace_bad_values(self, reference_array, array):
        wing = 5  # количество точек на которое делаем отступ от плохой точки, чтобы узнать дисперсию участка
        minimum = 0.01

        new_array = copy.deepcopy(array)

        for num, value in enumerate(new_array):
            if reference_array[num] != new_array[num]:
                continue

            sub_array_1 = new_array[num - wing: num + wing + 1]
            sub_array_2 = new_array[num - wing: num + wing + 1]

            try:
                sub_array_2[wing] = (sub_array_2[wing - 1] + sub_array_2[wing + 1]) / 2
            except:
                continue

            deviation_1 = numpy.var(sub_array_1)
            deviation_2 = numpy.var(sub_array_2)

            try:
                if deviation_2 / deviation_1 < minimum:
                    new_array[num] = sub_array_2[wing]
                    self._append_plot([self.get_array(TIME.T)[num: num + 3]], [new_array[num: num + 3]])
            except:
                logger.debug('Ошибка в функции замены плохих значений. {} / {}'.format(deviation_1, deviation_2))
                continue

        return new_array

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
        bad_areas = []

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

            identical_intervals = self.__get_identical_intervals(analog_intervals, digital_intervals, key, value, True)
            logger.debug('Идентичные интервалы у аналогового и цифрового наблюдения: %s' % identical_intervals)

            areas_by_observation[value] = identical_intervals
            bad_areas.extend(identical_intervals)
        return bad_areas
        # fi = self.(areas_by_observation)
        # logger.debug('Идентичные интервалы у наблюдений: %s' % fi)
        #
        # return self.__find_equal_areas_by_observations(areas_by_observation)

    def __find_bad_areas_old(self):
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

            identical_intervals = self.__get_identical_intervals(analog_intervals, digital_intervals, key, value, True)
            logger.debug('Идентичные интервалы у аналогового и цифрового наблюдения: %s' % identical_intervals)

            areas_by_observation[key] = identical_intervals
        equal_area = self.__find_equal_areas_by_observations_old(areas_by_observation)
        logger.debug(equal_area)
#        input()
        return self.__find_equal_areas_by_observations_old(areas_by_observation)

    def __delete_equal_areas(self, areas_by_observations):
        founded_intervals = []

        for observation in areas_by_observations:
            area = areas_by_observations[observation]

            founded_intervals = self.__update(founded_intervals, area)

        return founded_intervals

    def __find_equal_areas_by_observations_old(self, areas_by_observations):
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
            logger.debug(i)
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

    def __get_identical_intervals(self, intervals, other_intervals, key=None, num=None, flag=False):
        identical_intervals = []

        for interval in intervals:
            for other_interval in other_intervals:

                if self.__interval_is_identical(interval, other_interval):
                    if flag:
                        other_interval['observation'] = key
                        other_interval['observation_num'] = num
                    identical_intervals.append(other_interval)

        return identical_intervals

    @staticmethod
    def __interval_is_identical(interval, other_interval):
        return interval['begin'] == other_interval['begin'] and interval['end'] == other_interval['end']

    @staticmethod
    def plot_graph(x, y, name, plot):
        plot.scatter(x, y, s=5)
        plot.xlabel(r'$T$')
        plot.ylabel(r'$V$')
        plot.title('${0}$'.format(name.replace('_', '-')))
        plot.grid(True)
        plot.show()

    def _append_plot(self, x, y):
        self.plots.append(
            [x, y]
        )

    def prepare_plot(self, ploter):
        for x, y in self.plots:
            ploter.plot(
               x, y
            )
        return ploter


class WRITER:

    def __init__(self, file_name):
        self.name = file_name
        self.nsh_1 = (0., 0.)
        self.nsl_1 = (0., 0.)
        self.nsh_2 = (0., 0.)
        self.nsl_2 = (0., 0.)
        self.a_sys = (0., 0.)
        self.a_sour = (0., 0,)


    def write_result(self):
        tem = '\n'
        # tem += "#234567810123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234567130123456714012345671501234567160\n"
        # tem += "# Title, ch1     Year MM DD Year.XXX  NSH1_1   sig     NSL1_1   sig     NSH2_1   sig     NSL2_1   sig     A_sys    sig     A_sour   sig  F_sou   g       T_cal=\n"
        # tem += "#        ch2                          NSH1_2           NSL1_2           NSH2_2           NSL2_2                                          Jy              =T/g,K\n"
        # tem += "# ==============================================================================================================================================================\n"
        # tem += "#\n"
        G1, S1 = round(self.nsh_1[0], 3), round(self.nsh_1[1], 4)
        G2, S2 = round(self.nsl_1[0], 3), round(self.nsl_1[1], 4)
        G3, S3 = round(self.nsh_2[0], 3), round(self.nsh_2[1], 4)
        G4, S4 = round(self.nsl_2[0], 3), round(self.nsl_2[1], 4)
        A1, S5 = round(self.a_sys[0], 3), round(self.a_sys[1], 4)
        A2, S6 = round(self.a_sour[0], 3), round(self.a_sour[1], 4)
        tem += '%s 2018 08 09 0.0       %s     %s     %s      %s     %s      %s     %s      %s     %s       %s     %s     %s    0.0     0.0     0.0' % (
        self.name, G1, S1, G2, S2, G3, S3, G4, S4, A1, S5, A2, S6)
        log = self.create_result_file('result', 'result_file')

        fl = open(log, 'a')
        fl.write("%s\n" % (tem))
        fl.close()

    def create_result_file(self, type, name):
        name_folder = '%s' % type
        name_log = '%s.txt' % name
        current_log_directory = os.path.join(LOG_DIRECTORY, name_folder)
        log = os.path.join(current_log_directory, name_log)
        if not os.path.exists(current_log_directory):
            self.make_sure_path_exists(current_log_directory)
        return log

    def make_sure_path_exists(self, path):
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise


class Mark:
    begin = None
    end = None
    count = None


class Area:
    acceptable_percent_of_location = 10  # допустимый процент расхождения по расположению предполагамеого наблюдения
    acceptable_fraction_of_width = 10  # допустимый процент расхождения ширины предполагамого наблюдения
    acceptable_width_of_pillars = 15  # допустимый процент расхождения ширины одной полоски ГШ
    acceptable_abs_percent_of_width = 30

    def __init__(self, begin, end, count_begin, count_end, len_obs):
        self.begin = begin
        self.end = end
        self.left_pillar = count_begin
        self.right_pillar = count_end
        self.width = self.end - self.begin
        self.len_obs = len_obs

        self.pillars_average = (self.left_pillar + self.right_pillar) / 2
        self.pillar_deviation = abs(100 - (self.pillars_average * 100) / self.left_pillar)  # отклонение от среднего
        # pillar в процентаъ. Pillar это ширина одного ГША.
        self.abs_width = self.__get_abs_width()
        self.location = self.__get_location()
        self.fraction = self.__get_fraction()

    def __get_abs_width(self):
        return (self.width * 100) / self.len_obs

    def __get_location(self):
        return (self.begin * 100) / self.len_obs

    def __get_fraction(self):
        return (self.width * 100) / self.len_obs

    @staticmethod
    def is_close_location(obj, other):
        return abs(obj.location - other.location) <= Area.acceptable_percent_of_location

    @staticmethod
    def is_close_width(obj, other):
        return abs(100 - (obj.width * 100 / other.width)) <= Area.acceptable_abs_percent_of_width

    @staticmethod
    def is_close_pillars(obj, other):
        return abs(100 - (obj.right_pillar * 100 / other.right_pillar)) <= Area.acceptable_width_of_pillars and \
               abs(100 - (obj.left_pillar * 100 / other.left_pillar)) <= Area.acceptable_width_of_pillars

    def __eq__(self, other):
        return self.is_close_location(self, other) and self.is_close_width(self, other)# and self.is_close_pillars(self, other)

    def __str__(self):
        return 'Area <begin - {}, end - {},  width - {}, left pillar = {}, right pillar - {}>'.format(
            self.begin, self.end, self.width, self.left_pillar, self.right_pillar)


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
        logger.debug(elem)
        elem_sorted = sorted(elem, key=lambda x: elem[x], reverse=True)
        logger.debug(elem_sorted)
        #print(elem)
        if len(elem_sorted) > 2:
            elem = {elem_sorted[0]: elem.get(elem_sorted[0]), elem_sorted[1]: elem.get(elem_sorted[1])}
            #raise Exception('Элементов в массиве больше двух!')

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
            else:
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

        #self.__second_filter(array, marks)  # фильр для длинных интервалов, которые отличаются от всех остальных
        #logger.debug(array)

        try:
            for num, value in enumerate(marks):
                end = value['end']
                begin = marks[num + 1]['begin']
                logger.debug('Between %s - %s. Way - %s' % (num, num + 1, begin - end))
        except Exception as e:
            logger.debug(e)
            logger.debug('exit')

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
    a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    a = a[7-5:7+6]
    print(a)
    sred = (a[5-1] + a[5+1]) / 2
    a[5] = sred
    print(a, a[5-1], a[5+1])

    import matplotlib.pyplot as plt
    # a = [50, 48, 46, 55, 52, 55, 49, 50, 51, 55, 47]
    # a2 = [50, 51, 49, 50, 51, 100, 49, 50, 50, 49, 49]
    # t = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    # print(numpy.var(a2, ddof=1))
    # plt.scatter(t, a, s=5)
    # plt.xlabel(r'$x$')
    # plt.ylabel(r'$f(y)$')
    # plt.title(r'$y=$')
    # plt.grid(True)
    # plt.show()
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
