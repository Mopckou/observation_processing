import numpy
import logging
from src.approximater import ApproximationMethod
from src.helpers import INTERPRETER

logger = logging.getLogger('LOG')


class FinderGauss:
    def __init__(self, abscissa, ordinate, width_begin, width_end, windows, error_limit, step=1):
        self.abscissa = abscissa
        self.ordinate = ordinate
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

    def set_abscissa(self, array):
        self.abscissa = array

    def set_ordinate(self, array):
        self.ordinate = array

    def run(self):
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
            #self.__debug_plot(fits)
            fits = self.__filter_by_amplitude(fits)
            #self.__debug_plot(fits)
            fits = self.__filter_by_group(fits)  # апроксимации разбиваются по группам и возвращаются лучшие из групп
            #self.__debug_plot(fits)
            fits_by_width.append(fits)  # лучшие апроксимации добавляются в общий массив по всем ширинам

        # for i in fits_by_width:
        #     self.__debug_plot(i)
        best_fits = self.__find_best_of_the_best(fits_by_width)  # поиск лучших апроксимаций среди всех ширин
        self.__debug_plot(best_fits)
        return best_fits

    def handle_fits(self, fits):
        pass

    def __debug_plot(self, fits):
        plt.scatter(self.abscissa, self.ordinate, s=5)
        for fit in fits:
            coefficients = fit.coefficients
            x_segment = fit.x_segment
            width = fit.width
            x_zero = fit.x_zero
            y_new_segment = self.__approximate.get_new_segment(coefficients, x_segment, x_zero, width)

            plt.plot(x_segment, y_new_segment)
            print(fit.coefficients, fit.error, fit.amplitude)
        plt.xlabel(r'$x$')
        plt.ylabel(r'$f(y)$')
        plt.title(r'$y=$')
        plt.grid(True)
        plt.show()

    def prepare_plot(self, plot):

        for fit in self.fits:
            coefficients = fit.coefficients
            x_segment = fit.x_segment
            width = fit.width
            x_zero = fit.x_zero
            y_new_segment = self.__approximate.get_new_segment(coefficients, x_segment, x_zero, width)

            plot.plot(x_segment, y_new_segment)

        return plot

    def __fit(self, width):
        """
        Обработка файла наблденя на одной ширине.
        :param width: 
        :return: Возвращается массив. Каждый элемент массива СВД апроксимация.
        """
        fits = []
        fit_array = self.__approximate.fit(self.abscissa, self.ordinate, self.windows, width)

        for num, fit in enumerate(fit_array):
            hr = HandlingResult()

            hr.x_segment = self.abscissa[num: num + self.windows]
            hr.y_segment = self.ordinate[num: num + self.windows]
            hr.width = width
            hr.x_zero = fit[5]
            hr.error = fit[4]
            hr.coefficients = fit[:4]
            hr.amplitude = fit[6]
            # hr.y_segment_re_calc = self.__approximate.get_new_segment(
            #     hr.coefficients, hr.x_segment, hr.x_zero, hr.width
            # )

            fits.append(hr)

        return fits

    def __filter_by_error(self, fits):
        filtered = []

        for fit in fits:
            if fit.error is not None and fit.error < self.error_limit:# and fit.coefficients[3] > 0.03:
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
        amplitude = 0.01

        for fit in fits:
            fit.y_segment_re_calc = self.__approximate.get_new_segment(
                fit.coefficients, fit.x_segment, fit.x_zero, fit.width
            )
            fit.amplitude = self.__get_amplitude(fit)

            if fit.amplitude > amplitude:
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
                if self.__is_best(fit, best_of_the_best, fits_by_width, self.windows/3):
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

    def __get_amplitude(self, fit):
        begin_points = fit.y_segment_re_calc[:10]
        end_points = fit.y_segment_re_calc[-10:]

        begin_average = INTERPRETER.get_average(begin_points)
        end_average = INTERPRETER.get_average(end_points)
        average = INTERPRETER.get_average(
            [begin_average, end_average]
        )

        maximum = self.__approximate.func.calc_dot(
            fit.coefficients, fit.x_zero, fit.x_zero, fit.width
        )
        return maximum - average

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


class HandlingResult:

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

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from src.log import setup_logger
    from src.helpers import READER, TIME, DIGITAL, ANALOG

    setup_logger()
    file = 'out_6_92cm_spectr_20180110_133129_02_04_nomer_2.tmi'
    file2 = 'out_6_92cm_spectr_20180110_133129_02_04_nomer_2.tmi'
    file3 = 'out_6_92cm_spectr_20180124_004919_01_05_nomer_1.tmi'  # плохой файл
    file4 = 'out_6_92cm_spectr_20180212_180710_02_02_nomer_3.tmi'
    file5 = 'out_6_92cm_spectr_20180228_165341_01_02_nomer_4.tmi'  # готов
    file6 = 'out_6_92cm_spectr_20180309_161910_02_02.tmi'
    file7 = 'out_6_92cm_spectr_20180309_161910_02_02_nomer_5.tmi'
    reader = READER(file4)
    reader.parse()

    reader.cut_observation()
    reader.filter_digital_observation()
    reader.trim_to_seconds()
    reader.trim_bad_areas()

    x = reader.get_array(TIME.T)
    y = reader.get_array(ANALOG.OBSERVATION_18_K2)

    plt.scatter(x, y, s=5)
    plt.xlabel(r'$x$')
    plt.ylabel(r'$f(y)$')
    plt.title(r'$y=$')
    plt.grid(True)
    plt.show()
# 2.0560904      1.31027931E-02 -3.60823731E-04 -0.76090389       8.4285545       69193.000
    #fg = FinderGauss(x, y, 80, 200, 320, 0.8)
    #fg = FinderGauss(x, y, 1, 25, 100, 0.03)  # 6cm
    fg = FinderGauss(x, y, 1, 100, 140, 0.8)  # 18cm
    fg.run()

    print(fg.get_result(), fg.get_description())

    plt.scatter(x, y, s=5)
    fg.prepare_plot(plt)
    plt.xlabel(r'$x$')
    plt.ylabel(r'$f(y)$')
    plt.title(r'$y=$')
    plt.grid(True)
    plt.show()

    # 1. Починить разбивку на группы (если все плохие не брать первый)
    # 3. Добавить фильтр плохих вариантов с плохими коеффициентами
    # 4. Решить убирать фильрацию по амплитуде, поиграть с условием > 0.03
    # 5. Подсчет амплитуды сделать в SVD.exe
