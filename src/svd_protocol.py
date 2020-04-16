import time
import subprocess
import os
import logging

logger = logging.getLogger('LOG')

path_svd = "prog2.exe"
abs_path = os.path.join(
    os.path.normpath(os.path.split(__file__)[0]),
    path_svd
)


class PROCESSING:

    def __init__(self):
        self.query = ''

    def get_inquery(self, func, width, windows, coeff, count_point, x, y):
        query = '%s\n%s\n%s\n%s\n%s\n' % (func, width, windows, coeff, count_point)
        for value in x:
            query += '%s\n' % value
        for value in y:
            query += '%s\n' % value
        return query

    def parse_answer(self):
        try:
            logger.debug(self.out)
            self.out = self.out.decode('utf-8')
            #print(self.out)
            out_list = self.out.split('\r\n')
            logger.debug('count - %s' % len(out_list))
            if out_list[-1] != '':
                logger.debug(out_list[-1])
                raise
            self.coefficients = self.get_coefficient_list(out_list[:-1])  # перед коэффциентами в строке - пробелы
        except IndexError:
            logger.debug('Ответ от SVD не соответствует протоколу обмена.')
        except Exception as exc:
            logger.debug(exc)
            logger.debug('Не известная ошибка обработки ответа.')

    @staticmethod
    def convert_str_to_float(coefficients):

        converted_list = []
        for num, value in enumerate(coefficients):
            converted_list.append(float(value))

        return converted_list

    def get_coefficient_list(self, coefficients):
        new_coeff_list = []

        for cf in coefficients:
            coeff_list = cf.strip()
            new_coeff_list.append(self.convert_str_to_float(coeff_list.split()))

        return new_coeff_list

    def call_svd(self, inquiry):
        logger.debug(abs_path)
        before = time.time()
        sp = subprocess.Popen(abs_path, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              stdin=subprocess.PIPE)
        self.out, self.err = sp.communicate(inquiry.encode('utf-8'))
        after = time.time()
        logger.debug('%s svd sec' % (after - before))


if __name__ == '__main__':
    M = 9
    N = 3
    x = [1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980]
    A = [[0] * N for i in range(M)]


    Y = [[] for i in range(M)]
    Y[0] = 75.994575
    Y[1] = 91.972266
    Y[2] = 105.710620
    Y[3] = 123.203000
    Y[4] = 131.669275
    Y[5] = 150.697361
    Y[6] = 179.323175
    Y[7] = 203.211926
    Y[8] = 212.652030

    process = PROCESSING()
    inq = process.get_inquery(0, 0, 8, 3, 9, x, Y)
    print(inq)
    input()


    process.call_svd(inq)
    process.parse_answer()
    for num, coeff in enumerate(process.coefficients, 1):
        print(num, '=%s=' % coeff)
    input()
    # C = process.coefficients
    # import matplotlib.pyplot as plt
    #
    # t_axis = [1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970]
    # def func(t, a, b, c):
    #     return a + b * t + c * (t ** 2)
    # y_aprox = [func(i, C[0], C[1], C[2]) for i in t_axis]
    # """График"""
    # print(y_aprox)
    # plt.plot(t_axis, Y, t_axis, y_aprox)
    # plt.xlabel(r'$x$')
    # plt.ylabel(r'$f(x)$')
    # plt.title(r'$y=gussian123$')
    # plt.grid(True)
    # plt.show()