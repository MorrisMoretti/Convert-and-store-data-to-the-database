import pytest

from tests.conftest import DRIVER1, DRIVER2, DRIVER3, FULL_DATA
from web_report.api_racer import RacersManager, driver_enum


def test_driver_enum():
    assert driver_enum([(1, next(iter(FULL_DATA))['driver_info'])]) == FULL_DATA


@pytest.mark.parametrize('param, expected_result', [('asc', [DRIVER1, DRIVER2, DRIVER3]),
                                                    ('desc', [DRIVER3, DRIVER2, DRIVER1])])
def test_get_drivers(use_db, pop_db, remove_db, param, expected_result):
    for fun_ret, ex_result in zip(RacersManager.get_drivers(direction=param), expected_result):
        assert ex_result.driver == fun_ret['driver_info']['driver']


@pytest.mark.parametrize('param, expected_result',
                         [('SVF', next(iter(FULL_DATA))['driver_info']),
                          ('Fake_Name', [])])
def test_data_code(use_db, pop_db, param, expected_result):
    assert str(expected_result) in str(RacersManager.data_code(param))
