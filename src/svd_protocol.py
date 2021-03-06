import time
import subprocess
import os
import logging
import sys

logger = logging.getLogger('LOG')

path_svd = "newprog"
if sys.platform.lower().startswith('win'):
    path_svd = "Ermakov.exe"

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
            #if os.system()
            #out_list = self.out.split('\r\n')
            out_list = self.out.split('\n')
            logger.debug('count - %s' % len(out_list))
            # import pdb
            # pdb.set_trace()
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
