import pytest
from src.helpers import WRITER, TIME, OBSERVATIONS
from src.finder_gsh import GshOPERATOR
from tests.processed_data import NS


def get_processed_data(reader, observation):
    operator = GshOPERATOR()
    operator.set_reader(reader)

    original_y = reader.get_original_array(observation)

    observation_name = reader.get_name_observation(observation)

    if not reader.meaningful_data(original_y):
        print('Файл %s пустой.' % observation_name)
        return

    operator.find_gsh(observation)
    return operator.get_report()


def test_ns(env):
    cases = NS[env.file_name].keys()

    for observation in cases:
        data = get_processed_data(env, observation)

        ans = NS[env.file_name][observation]
        assert ans == data
