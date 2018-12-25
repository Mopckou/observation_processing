import logging
from src.helpers import GshB, GshH, ANALOG, DIGITAL, INTERPRETER

logger = logging.getLogger('LOG')


class ErrorVerifyGSHA(Exception):
    pass


class GshParser:

    def __init__(self):
        self.__result = None
        self.__description = ''
        self.ordinate = []
        self.abscissa = []
        self.gsh_B = {}
        self.gsh_H = {}

    def set_gsh_H(self, table, channel, value):
        self.gsh_H[channel] = {
                    'table': table,
                    'value': value
                }

    def set_gsh_B(self, table, channel, value):
        self.gsh_H[channel] = {
                    'table': table,
                    'value': value
                }

    @staticmethod
    def verify(obj):
        array = obj['value']
        table = obj['table']
        logger.info('ПРОВЕРКА МАССИВА НА КОРРЕКТНОЕ КОЛИЧЕСТВО ГША. НОМЕР СТОЛБЦА - %s' % table)

        count = INTERPRETER.count_on_interval(array)
        logger.info('Количество ГША - %s' % count)

        result = count == 2 or count == 1
        logger.info('Результат проверки - %s' % result)
        return result

    def check_gha(self):
        all_gsha = {}
        all_gsha.update(self.gsh_H)
        all_gsha.update(self.gsh_B)

        for value in all_gsha:
            obj = all_gsha[value]
            result = self.verify(obj)
            if not result:
                raise ErrorVerifyGSHA

    def set_ordinate(self, value):
        self.ordinate = value

    def set_abscissa(self, value):
        self.abscissa = value

    def run(self):
        try:
            self.check_gha()
        except ErrorVerifyGSHA:
            self.__set_result(False, 'Недопустимое количество ГША!')
            return
        except Exception as e:
            logger.exception(e)
            self.__set_result(False, 'Ошибка в ходе проверки ГША!')
            return
        else:
            self.__set_result(True, 'Ошибок нет.')



    def build_graph(self):
        pass

    def __set_result(self, result, description):
        self.__result = result
        self.__description = description

    def get_error_code(self):
        return self.__result

    def get_description(self):
        return self.__description

    def write_result(self):
        pass
