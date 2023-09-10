import numpy
import logging
from src.approximater import ApproximationMethod
from src.helpers import INTERPRETER, READER
from src.gnuplot import generate_gnuplot_graf

logger = logging.getLogger('LOG')


class FinderGauss:
    def __init__(self, abscissa, ordinate, null, width_begin, width_end, windows, error_limit, step=1):
        self.abscissa = abscissa
        self.ordinate = ordinate
        self.null = null
        self.width_begin = width_begin
        self.width_end = width_end
        self.windows = windows
        self.error_limit = error_limit
        self.step = step
        self.__result = False
        self.__description = ''
        self.__approximate = ApproximationMethod()
        self.__approximate.set_function('gauss')
        self.fits = []
        self.__report = {}

    def set_abscissa(self, array):
        self.abscissa = array

    def set_ordinate(self, array):
        self.ordinate = array

    def find_gauss(self):
        self.fits = self.process_observation()

        if len(self.fits) == 0:
            self.__set_result(False, 'Не найден ни один отклик!')
            return

        if self.handle_fits(self.fits):
            self.__set_result(True, 'Ошибок нет.')
            return

    def process_observation(self):
        fits_by_width = []

        for width in numpy.arange(self.width_begin, self.width_end, self.step):
            fits = self.__fit(width)  # обработка файла на одной ширине

            fits = self.__filter_by_error(fits)  # фильтруются апроксимации с ошибкой большей допустимой
            # # TODO удалить
            # if width == 112:
            #     self.fits0 = self.calculate_model_fits(fits=fits)
            fits = self.__filter_by_amplitude(fits)

            fits = self.__filter_by_group(fits)  # апроксимации разбиваются по группам и возвращаются лучшие из групп

            fits_by_width.append(fits)  # лучшие апроксимации добавляются в общий массив по всем ширинам

        best_fits = self.__find_best_of_the_best(fits_by_width)  # поиск лучших апроксимаций среди всех ширин
        best_fits = self.__filter_excess_elements(best_fits)  # фильтрация лишних элементов
        best_fits = self.__filter_unnecessary_fits(best_fits)

        return best_fits

    def handle_fits(self, fits):
        amplitude_list = []

        fits = sorted(fits, key=lambda elem: elem.x_zero)

        for fit in fits:
            # s, e = self.__get_sys(fit, deviation_percent=True, f=False)
            # if e > 1:
            #     continue
            # breakpoint()
            maxi = self.__approximate.get_new_segment(fit.coefficients, [fit.x_zero], fit.x_zero, fit.width)[0]
            sys = self.__get_sys(fit, begin_points=10, end_points=10)  # 0.0306327343 0.02882219

            print(maxi, sys, maxi - sys, fit.x_zero, fit.coefficients, fit.amplitude)  # 58134.0

            amplitude_list.append(
                maxi - sys  # fit.amplitude
            )
        # [0.02263826260567836, 0.02815849311778207, 0.025488162025318895]
        # [0.02315183575551505, 0.026669386307034193, 0.023431774177149478]
        # [0.020872510680330136, 0,02521959926375672, 0,02394360449329347]
        # [0.018926639366411147, 0,027781655205677658, 0,022553886309640503]

        #if len(amplitude_list) > 1:
        count = len(amplitude_list) // 2
        left = amplitude_list[:count]
        right = amplitude_list[count:]

        max_left = max(left)
        max_right = max(right)
        max_left_index = amplitude_list.index(max_left)
        max_right_index = amplitude_list.index(max_right)
        print(max_left_index)
        print(max_right_index)
        #breakpoint()
        l = self.get_slice(amplitude_list, max_left_index)
        r = self.get_slice(amplitude_list, max_right_index)
        print(l)
        print(r)

        #breakpoint()
        if len(l) == 2:
            pass
        else:
            average11 = abs(l[0] - l[1])
            average12 = abs(l[1] - l[2])
            if average11 < average12:
                l = l[:2]
            else:
                l = l[1:]

        if len(r) == 2:
            pass
        else:
            average21 = abs(r[0] - r[1])
            average22 = abs(r[1] - r[2])
            if average21 < average22:
                r = r[:2]
            else:
                r = r[1:]

        average1 = INTERPRETER.get_average(l)
        sigma1 = INTERPRETER.get_sigma(l)
        percent1 = INTERPRETER.get_percent(sigma1, average1)

        average2 = INTERPRETER.get_average(r)
        sigma2 = INTERPRETER.get_sigma(r)
        percent2 = INTERPRETER.get_percent(sigma2, average2)

            # f = self.fits[max_left_index]
            # s, e = self.__get_sys(self.fits[max_left_index-1], deviation_percent=True)
            # print(s, e)
            # s, e = self.__get_sys(self.fits[max_left_index], deviation_percent=True)
            # print(s, e)
            # s, e = self.__get_sys(self.fits[max_left_index+1], deviation_percent=True)
            #
            # print(s, e)
        if average1 > average2:
            amplitude_list = l
        else:
            amplitude_list = r
            #breakpoint()
        if percent1 > 11:
            amplitude_list = r
        elif percent2 > 11:
            amplitude_list = l


        average = INTERPRETER.get_average(amplitude_list)
        sigma = INTERPRETER.get_sigma(amplitude_list)
        percent = INTERPRETER.get_percent(sigma, average)
        self.__report['sour'] = {
            'average': average,
            'sig': percent
        }

        sys_list = []
        for fit in fits:
            sys_list.append(
                self.__get_sys(fit)
            )

        sys_average = INTERPRETER.get_average(sys_list)
        sys_sigma = INTERPRETER.get_sigma(sys_list)
        sys_percent = INTERPRETER.get_percent(sys_sigma, sys_average)

        logger.info('Отнимаем аппаратный ноль: {} - {} = {}'.format(sys_average, self.null, sys_average - self.null))

        self.__report['sys'] = {
            'average': sys_average - self.null,
            'sig': sys_percent
        }

        return True

    def get_slice(self, array, index):
        count = len(array)
        li = index - 1 if index - 1 >= 0 else index
        ri = index + 2 if index + 1 <= count else index + 1
        return array[li:ri]

    def set_plot_manager(self, plt):
        self.plt = plt

    def __debug_plot(self, fits):
        self.plt.scatter(self.abscissa, self.ordinate, s=5)
        for fit in fits:
            coefficients = fit.coefficients
            x_segment = fit.x_segment
            width = fit.width
            x_zero = fit.x_zero
            y_new_segment = self.__approximate.get_new_segment(coefficients, x_segment, x_zero, width)

            self.plt.plot(x_segment, y_new_segment)
            print(fit.coefficients, fit.error, fit.amplitude)
        self.plt.xlabel(r'$x$')
        self.plt.ylabel(r'$f(y)$')
        self.plt.title(r'$y=$')
        self.plt.grid(True)
        self.plt.show()

    def prepare_plot(self, plot):
        for x_segment, y_new_segment in self.calculate_model_fits():
            plot.plot(x_segment, y_new_segment)

        return plot

    def calculate_model_fits(self, x=None, many=False, only_source=True, fits=None):
        fits = fits if fits else self.fits
        model_fits = []

        for fit in fits:
            coefficients = fit.coefficients
            x_segment = fit.x_segment
            width = fit.width
            x_zero = fit.x_zero
            if many:
                x_index = x.index(x_zero)

                x_segment = x[x_index - 300: x_index + 250]

            y_new_segment = self.__approximate.get_new_segment(coefficients, x_segment, x_zero, width, only_source)
            model_fits.append(
                (x_segment, y_new_segment)
            )

        return model_fits

    def noise_90cm(self, fits):
        print(fits[0])

        new_fit = []
        for fit in fits:
            x_segmen = fit[0]
            y_segment = fit[1]
            x, x0 = x_segmen[-1], x_segmen[0]
            y, y0 = y_segment[-1], y_segment[0]
            coeff = (y - y0)/(x - x0)
            yyy = y0 - coeff*x0
            print(coeff)
            fx = []
            fy = []
            for nx in fit[0]:
                fx.append(
                    nx
                )

                fy.append(nx*coeff + yyy)
            print(fx)
            print(fy)
            new_fit.append(
                (fx, fy)
            )# 37497, 37498, 37499

        return new_fit

    def __fit(self, width):
        """
        Обработка файла наблденя на одной ширине.
        :param width: 
        :return: Возвращается массив. Каждый элемент массива СВД апроксимация.
        """
        fits = []
        fit_array = self.__approximate.fit(
            self.abscissa, self.ordinate, self.windows, width
        )

        for num, fit in enumerate(fit_array):
            ft = Fit()

            ft.x_segment = self.abscissa[num: num + self.windows]
            ft.y_segment = self.ordinate[num: num + self.windows]
            ft.width = width
            ft.x_zero = fit[5]
            ft.error = fit[4]
            ft.coefficients = fit[:4]
            ft.amplitude = fit[6]

            fits.append(ft)

        return fits

    def __filter_by_error(self, fits):
        filtered = []

        for fit in fits:
            if fit.error is not None and fit.error < self.error_limit:
                filtered.append(fit)
        return filtered

    @staticmethod
    def split_into_groups(fits):
        groups = []

        if not fits:
            return []

        group = [fits[0]]  # первый эелемент добавляем сразу в первую группу
        for num in range(1, len(fits)):
            if fits[num].x_zero - fits[num - 1].x_zero == 1:
                group.append(fits[num])
            else:
                groups.append(
                    group  # добавляем группку в массив групп
                )
                group = [fits[num]]  # начинаем заполнять новую группу

        if group:
            groups.append(group)

        return groups

    def __filter_by_group(self, fits):
        filtered = []
        groups = self.split_into_groups(fits)

        for group in groups:
            best_fit = self.__find_best_fit_in_group(group)
            filtered.append(best_fit)
            print(best_fit, best_fit.amplitude)

        return filtered

    def __filter_by_amplitude(self, fits):
        filtered = []
        min_amplitude = 0.01

        for fit in fits:

            if fit.amplitude > min_amplitude:
                filtered.append(fit)

        return filtered

    def __find_best_fit_in_group(self, group):
        best = group[0]

        for fit in group:
            if fit.amplitude > best.amplitude:
                best = fit

        return best

    def __find_best_of_the_best(self, fits_by_width):
        best_of_the_best = []

        for num, fits in enumerate(fits_by_width):
            for fit in fits:
                if self.__is_best(fit, best_of_the_best, fits_by_width, self.windows/4):
                    best_of_the_best.append(fit)

        return best_of_the_best

    def __is_best(self, compared_fit, best_of_the_best, fits_by_width, windows):
        x_zero = compared_fit.x_zero
        error = compared_fit.error

        for fit in best_of_the_best:  # сначала проверяем есть ли в массиве лучших похожий элемент на compared_fit
            new_x_zero = fit.x_zero
            if self.__is_equally_location(x_zero, new_x_zero, windows):
                # если в массиве лучших апроксимаций, уже есть элемент с похожим расположением
                # то compared_fit не самый лучший элемент
                return False

        for fits in fits_by_width:  # ищем элемент который лучше чем compared_fit
            for fit in fits:
                new_x_zero = fit.x_zero
                if self.__is_equally_location(x_zero, new_x_zero, windows) and fit.error < error:
                    # если есть элемент с похожим росположением в файле и меньшей ошибкой, то данный compared_fit
                    # не самый лучший, поэтому возвращается False
                    return False

        return True  # если поиск не удовлетворен, то compared_fit лучший

    def __filter_excess_elements(self, fits):
        array_of_comparisons = []
        for num, value in enumerate(fits):
            array_of_comparisons.append(
                (value, self.__get_comparisons(num, value, fits))
            )  # получить сравнение со всеми эелементами fits
        print('Fits с массивом сравнений %s' % array_of_comparisons)

        filtered_elements = []
        for num, value in enumerate(array_of_comparisons):
            comparisons = value[1]
            if comparisons != [] and not self.__is_superfluous_expression(comparisons):
                filtered_elements.append(value[0])

        return filtered_elements

    @staticmethod
    def __filter_unnecessary_fits(fits):
        logger.debug('Амплитуды: \n%s' % (
            '\n-------------------------\n'.join(READER.prepare_for_log(fits))))
        groups = READER.break_down_into_groups(fits)
        logger.debug('Сгруппированные предполагамемые амплитуды: \n%s' % (
            '\n-------------------------\n'.join(READER.prepare_for_log(group) for group in groups)))

        sorted_group = sorted(groups, key=lambda x: len(x))
        if not sorted_group:
            return []
            #raise Exception('Не найдено ниодной амплитуды!')

        logger.debug('Найденная группа: \n%s' % READER.prepare_for_log(sorted_group[-1]))
        return sorted_group[-1]

    def __is_superfluous_expression(self, comparisons):
        excess = True

        for value in comparisons:
            if value < 25:
                excess = False

        return excess

    def __get_comparisons(self, number, fit, fits):
        comparisons = []
        amplitude = fit.amplitude

        for num, value in enumerate(fits):
            other_amplitude = value.amplitude
            percent = abs(100 - INTERPRETER.get_percent(amplitude, other_amplitude))
            if num != number:
                comparisons.append(percent)

        return comparisons

    def __get_sys(self, fit, deviation_percent=False, begin_points=10, end_points=10, f=True):
        y_new = self.__approximate.get_new_segment(fit.coefficients, fit.x_segment, fit.x_zero, fit.width)

        if f:
            begin_points = y_new[begin_points:begin_points + 5]
            end_points = y_new[-(end_points + 5):-end_points]
        else:
            begin_points = y_new[:begin_points]
            end_points = y_new[-end_points:]

        logger.debug(begin_points)
        logger.debug(end_points)

        begin_average = INTERPRETER.get_average(begin_points)
        end_average = INTERPRETER.get_average(end_points)

        logger.debug('begin aver = %s' % begin_average)
        logger.debug('end aver = %s' % end_average)

        average = INTERPRETER.get_average(
            [begin_average, end_average]
        )

        logger.debug('average = %s' % average)
        if deviation_percent:
            return average, abs(100 - INTERPRETER.get_percent(begin_average, average))

        return average

    def __get_deviation_sys_level(self, fit):
        y_new = self.__approximate.get_new_segment(fit.coefficients, fit.x_segment, fit.x_zero, fit.width)
        begin_points = y_new[:10]
        end_points = y_new[-10:]

        logger.debug(begin_points)
        logger.debug(end_points)

        begin_average = INTERPRETER.get_average(begin_points)
        end_average = INTERPRETER.get_average(end_points)

        logger.debug('begin aver = %s' % begin_average)
        logger.debug('end aver = %s' % end_average)

        average = INTERPRETER.get_average(
            [begin_average, end_average]
        )

        logger.debug('average = %s' % average)

        return average



    @staticmethod
    def __is_equally_location(x_zero, new_x_zero, windows):
        return new_x_zero == x_zero or abs(new_x_zero - x_zero) < windows

    def __set_result(self, result, description):
        self.__result = result
        self.__description = description

    def get_result(self):
        return self.__result

    def get_description(self):
        return self.__description

    def get_report(self):
        return self.__report


class Fit:
    acceptable_abs_percent_of_amplitude = 45  # допутимый процент расхождения по амлитуде

    def __init__(self):
        self.x_zero = None
        self.x_segment = []
        self.y_segment = []
        self.width = None
        self.coefficients = []
        self.error = None
        self.y_segment_re_calc = []
        self.amplitude = 0.

    def __repr__(self):
        return 'X0: %s; Width: %s; Error: %s, Coefficients: %s, amplitude: %s' % (
            self.x_zero, self.width, self.error, self.coefficients, self.amplitude
        )

    def __eq__(self, other):
        return self.__is_close_amplitude(self, other)

    @staticmethod
    def __is_close_amplitude(obj, other):
        return abs(100 - (obj.amplitude * 100 / other.amplitude)) <= Fit.acceptable_abs_percent_of_amplitude


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from src.log import setup_logger
    from src.helpers import READER, TIME, DIGITAL, ANALOG

    setup_logger()
    file1 = 'out_6_92cm_spectr_20180309_161910_02_02.tmi'
    file = 'out_6_92cm_spectr_20180110_133129_02_04_nomer_2.tmi'
    file2 = 'out_6_92cm_spectr_20180110_133129_02_04_nomer_2.tmi'
    file3 = 'out_6_92cm_spectr_20180124_004919_01_05_nomer_1.tmi'  # плохой файл
    file4 = 'out_6_92cm_spectr_20180212_180710_02_02_nomer_3.tmi'
    file5 = 'out_6_92cm_spectr_20180228_165341_01_02_nomer_4.tmi'  # готов
    file6 = 'out_6_92cm_spectr_20180309_161910_02_02.tmi'
    file7 = 'out_6_92cm_spectr_20180309_161910_02_02_nomer_5.tmi'
    reader = READER(file5)
    reader.parse()

    reader.cut_observation()
    reader.filter_digital_observation()
    reader.trim_to_seconds()
    reader.trim_bad_areas()
    #reader.handle_observation(reader.get_array(ANALOG.OBSERVATION_18_K2))

    x = reader.get_array(TIME.T)
    y = reader.get_array(DIGITAL.OBSERVATION_18_K2)

    plt.scatter(x, y, s=5)
    plt.plot([62517], [-0.1])
    plt.xlabel(r'$x$')
    plt.ylabel(r'$f(y)$')
    plt.title(r'$y=$')
    plt.grid(True)
    plt.show()

    yd6_2 = reader.get_array(DIGITAL.OBSERVATION_6_K2)
    ya6_2 = reader.get_array(ANALOG.OBSERVATION_6_K2)

    yd18_1 = reader.get_array(DIGITAL.OBSERVATION_18_K1)
    ya18_1 = reader.get_array(ANALOG.OBSERVATION_18_K1)

    yd18_2 = reader.get_array(DIGITAL.OBSERVATION_18_K2)
    ya18_2 = reader.get_array(ANALOG.OBSERVATION_18_K2)

    yd92_1 = reader.get_array(DIGITAL.OBSERVATION_92_K1)
    ya92_1 = reader.get_array(ANALOG.OBSERVATION_92_K1)

    yd92_2 = reader.get_array(DIGITAL.OBSERVATION_92_K2)
    ya92_2 = reader.get_array(ANALOG.OBSERVATION_92_K2)

    a = []
    for num, value in enumerate(yd18_2):
        if yd18_2[num] == ya18_2[num]:
            array1 = yd18_2[num - 5: num + 5 + 1]
            array2 = yd18_2[num - 5: num + 5 + 1]
            try:
                srednee = (array2[5 - 1] + array2[5 + 1]) / 2
                array2[5] = srednee
            except:
                continue
            var1 = numpy.var(array1)
            var2 = numpy.var(array2)
            zamena = var2/var1 < 0.01
            print(x[num], yd18_2[num], num, var1, var2, zamena)
    # reader.replace_bad_values()
    # x = reader.get_array(TIME.T)
    # y = reader.get_array(DIGITAL.OBSERVATION_6_K2)
    # plt.scatter(x, y, s=5)
    # plt = reader.prepare_plot(plt)
    # plt.xlabel(r'$x$')
    # plt.ylabel(r'$f(y)$')
    # plt.title(r'$y=$')
    # plt.grid(True)
    # plt.show()

    # 1. Починить разбивку на группы (если все плохие не брать первый)
    # 3. Добавить фильтр плохих вариантов с плохими коеффициентами
