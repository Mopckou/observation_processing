import os
import datetime
from configparser import ConfigParser
import matplotlib.pyplot as plt
from src.log import setup_logger
from src.helpers import READER, DIGITAL, ANALOG, TIME, WRITER, OBSERVATIONS
from src.finder_gsh import GshOPERATOR
from src.finder_gauss import FinderGauss
from tests.processed_data import *

import pytest
TESTS = NS.keys()


@pytest.fixture(
    params=TESTS,
    ids=TESTS
)
def env(request):

    #setup_logger()
    LOG_DIRECTORY = os.path.join(os.getcwd(), 'OUT')
    reader = READER('..//IN//' + request.param)
    reader.file_name = request.param
    reader.parse()

    reader.cut_observation()  # обрезаем лишние участки когда наблюдение не ведется
    reader.filter_digital_observation()  # фильтрация цифровых наблюдений на основе аналогового наблюдения
    reader.trim_to_seconds()  # изначально файл в милисекундах, обрезаем файл до секунд
    reader.trim_bad_areas()  # удаление нулевых участков
    reader.replace_bad_values()

    return reader
