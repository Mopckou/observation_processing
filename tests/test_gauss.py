from src.finder_gauss import FinderGauss
from src.helpers import TIME, SETUP
from tests.processed_data import GS


def get_processed_data(reader, observation):
    x = reader.get_time(observation)
    y = reader.get_array(observation)
    finder = FinderGauss(x, y, *SETUP[observation])  # TODO отнять аппаратный ноль!!!
    finder.find_gauss()

    return finder.get_report()


def test_gauss(env):
    cases = GS[env.file_name].keys()

    for observation in cases:
        data = get_processed_data(env, observation)

        ans = GS[env.file_name][observation]
        assert ans == data
