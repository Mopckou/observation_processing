from src.function import FUNCTION
from src.svd_protocol import PROCESSING
import os


class APPROXIMATE:

    def fit(self, *args, **kwargs):
        pass

    @staticmethod
    def get_error(y_original, y_fit):
        amount = 0
        for num, value in enumerate(y_fit):
            amount += (value - y_original[num]) ** 2
        return amount

    def get_new_segment(self, *args, **kwargs):
        pass


class ApproximationMethod(APPROXIMATE):
    function = 'right_angled'

    def __init__(self):
        self.func = FUNCTION(self.function)
        self.process = PROCESSING()

    def set_function(self, function):
        self.func.set_function(function)

    def fit(self, x, y, windows, width):
        inq = self.get_full_query(x, y, windows, width)

        self.process.call_svd(inq)
        self.process.parse_answer()
        #print(len(self.process.coefficients))
        return self.process.coefficients

    def get_full_query(self, x, y, windows, width):
        func_list = {'right_angled': 0, 'gauss': 1}
        count = len(x)
        inq = self.process.get_inquery(func_list[self.func.name_func], width, windows, 4, count, x, y)
        return inq

    def get_new_segment(self, coeff, x, t_nul, width, with_source=True):
        if with_source:
            return self.func.get_new_segment(coeff, x, t_nul, width)

        return self.func.get_noise_segment(coeff, x, t_nul)


if __name__ == '__main__':

    a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    print(a[:10])