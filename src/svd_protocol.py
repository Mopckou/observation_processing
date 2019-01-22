import time
import subprocess
import os

path_svd = "other\Ermakov.exe"
abs_path = os.path.join(
    os.path.normpath(os.path.split(__file__)[0]),
    path_svd
)
# 10594721.
# 3.48304602E-04
# 64.776894
# -1.67051819E-03 - 1.6161451
# 8.70477757E-04

# 11296800.
# 4.66040510E-04
# 77.420181
# -1.66409556E-03 - 1.6142638
# 8.69419717E-04
#1.97377760742e-08, coeff - [3.0000038, -6.92836579e-08, 3.56176244e-08, 2.0000002]
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
            print(111, self.out)
            self.out = self.out.decode('utf-8')
            #print(self.out)
            out_list = self.out.split('\r\n')
            print('count - %s' % len(out_list))
            if out_list[-1] != '':
                print(out_list[-1])
                raise
            self.coefficients = self.get_coefficient_list(out_list[:-1])  # перед коэффциентами в строке - пробелы
        except IndexError:
            print('Ответ от SVD не соответствует протоколу обмена.')
        except Exception as exc:
            print(exc)
            print('Не известная ошибка обработки ответа.')

    def convert_str_to_float(self, list):
        convert_list = []
        for i in range(len(list[:-1])):
            convert_list.append(float(list[i]))
        convert_list.append(list[-1])
        return convert_list

    def get_coefficient_list(self, coeff):
        new_coeff_list = []
        for cf in coeff:
            coeff_list = cf.strip()
            new_coeff_list.append(self.convert_str_to_float(coeff_list.split()))
        return new_coeff_list

    def call_svd(self, inquiry):
        print(abs_path)
        before = time.time()
        sp = subprocess.Popen(abs_path, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              stdin=subprocess.PIPE)
        self.out, self.err = sp.communicate(inquiry.encode('utf-8'))
        after = time.time()
        print('%s svd sec' % (after - before))
#   1.04008386E-07 -4.56198526E-04  2.82839610E-04  2.92764674E-10
# 0.000363420608, coeff - [2.999984, 4.34724576e-08, -7.98098725e-08, -0.50000048], important_section - True
# 0.0003636370087959139, coeff - [2.999984, 4.34724576e-08, -7.98098725e-08, -0.50000048], important_section - True
# 5.56352692923e-08, coeff - [3.0000179, 6.26983905e-08, -9.89562139e-08, -0.50000036]

# 0.000370624184, coeff - [2.9999843, -2.3858891e-07, -8.21031776e-08, 1.9999983]
# 0.0003703690528451533, coeff - [2.9999843, -2.3858891e-07, -8.21031776e-08, 1.9999983],
# 1.52877898447e-07, coeff - [3.0000169, -2.09609965e-07, -1.46426032e-07, 2.0]

#0.000365061598, coeff - [2.999984, -7.68492043e-08, -8.02746314e-08, 0.49999893]
#0.0003654033123193207, coeff - [2.999984, -7.68492043e-08, -8.02746314e-08, 0.49999893
#8.55021267758e-08, coeff - [3.0000167, -3.53750913e-08, -1.15797249e-07, 0.49999923]

#0.0002924074670315261, coeff - [3.0000167, -3.53750913e-08, -1.15797249e-07, 0.49999923]
#0.000608139962, coeff - [2.9999981, -7.31677829e-08, 3.52402836e-08, 1.0000002]
#error - 0.0006073429748596689, coeff - [2.9999983, -7.32259906e-08, 3.51238683e-08, 0.99999994]
#3.9960193524115316e-05, coeff - [2.9999983, 4.07382821e-08, -1.27607613e-09, 1.0000005],
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