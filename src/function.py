import math


class FUNCTION:
    def __init__(self, name_function=None):
        if name_function is not None:
            self.name_func = name_function
        else:
            self.name_func = 'right_angled'

    def set_function(self, name):
        self.name_func = name

    def get_matrix_plane(self, t, t_nul, width):
        """
        Функция подсчета матрицы плана
        :param t: 
        :param t_nul: 
        :param width: 
        :return: 
        """
        func = self.right_angled if self.name_func == 'right_angled' else self.gussian_function
        A = []
        a = []
        for i in range(len(t)):
            a.append(1.)
            a.append(
                self.delta(t[i], t_nul)
            )
            a.append(
                self.delta(t[i], t_nul) * self.delta(t[i], t_nul)
            )
            a.append(
                func(t[i], t_nul, width)
            )
            A.append(a)
            a = []
        return A

    @staticmethod
    def delta(t, t_nul):
        return t - t_nul

    @staticmethod
    def right_angled(t, t_nul, width):
        width_new = width / 2.
        if t >= (t_nul - width_new) and t <= (t_nul + width_new):
            return 1.
        else:
            return 0.

    @staticmethod
    def gussian_function(x, x0, a0):
        def func_lambda(x):
            #return -((x-x0)*(x-x0) / 100 * a0 * a0)
            return -((x - x0) * (x - x0) / (a0 * a0))
        a = (1 / (a0 * math.sqrt(2 * math.pi)))
        e = pow((math.e), func_lambda(x))
        #return ((1 / (a0 * math.sqrt(2 * math.pi))) * pow((math.e), func_lambda(x)))

        return pow((math.e), func_lambda(x))
#7, 7, 6, 6 |  116, 116, 112, 114 - K2 92 | 116, 105, 105, 100 - K2 | ---- 18, 19, 17, 18 - K1 18 | 18, 19, 18, 18 - K2 18
    def calc_dot(self, c, t, t_nul, width):
        func = self.right_angled if self.name_func == 'right_angled' else self.gussian_function
        return c[0] * 1. + c[1] * (t - t_nul) + c[2] * pow((t - t_nul), 2) + c[3] * func(t, t_nul, width)

    def calc_noise_level(self, c, t, t_nul):
        return c[0] * 1. + c[1] * (t - t_nul) + c[2] * pow((t - t_nul), 2)

    def get_noise_segment(self, c, x, t_nul):
        return [self.calc_noise_level(c, i, t_nul) for i in x]

    def get_new_segment(self, c, x, t_nul, width):
        """
        Функция возвращает отрезок ординаты Y, пересчитанный по новым коэффициентам 
        :param c: коэффциенты
        :param t_nul: середина окна
        :param width: ширина (для прямоугольной функции это ширина единичной площадки, для гауссианы a0 )
        :param x: отрезок ординаты X
        :return: отрезок ординаты Y
        """
        return [self.calc_dot(c, i, t_nul, width) for i in x]

if __name__ == '__main__':
    gauss_group = []

    gauss_list = [0, 3, 5, 7, 9, 10, 12, 13, 14, 20, 22, 23, 28]

    group = [gauss_list[0]]
    for num in range(1, len(gauss_list)):
        print(num)
        print(gauss_list[num - 1] - gauss_list[num])
        if gauss_list[num] - gauss_list[num - 1] == 1:
            group.append(gauss_list[num])
        else:
            gauss_group.append(group)
            group = [gauss_list[num]]

    if group != []:
        gauss_group.append(group)
    for i in gauss_group:
        print(i)
    print('____')
    final_list = []
    for gr in gauss_group:
        best = gr[0]
        for i in gr:
            if i > best:
                best = i
        final_list.append(best)
    print(final_list)

