from unittest import mock
from unittest.mock import MagicMock, mock_open, patch

import pytest
from peewee import SqliteDatabase

from app import Config
from app import app as flask_app
from web_report import Racer, RacingDataAnalyzer
from web_report.models import RaceResult

PATH = 'path/to/open'
FILES = {'path/to/open/start.log': 'SVF2018-05-24_12:02:58.917',
         'path/to/open/end.log': 'SVF2018-05-24_12:04:03.332',
         'path/to/open/abbreviations.txt': 'SVF_Sebastian Vettel_FERRARI'}
DRIVER1 = Racer(lap_time='0:01:04.415000', car='FERRARI', driver='Sebastian Vettel', abr='SVF')
DRIVER2 = Racer(lap_time='0:01:12.657000', car='MCLAREN RENAULT', driver='Fernando Alonso', abr='FAM')
DRIVER3 = Racer(lap_time='0:01:13.065000', car='RENAULT', driver='Nico Hulkenberg', abr='NHR')
DATA = [DRIVER1, DRIVER2, DRIVER3]
DATA_VALUE = ['0:01:04.415000', 'FERRARI', 'Sebastian Vettel', 'SVF']
FULL_DATA = [{'position': 1,
              'driver_info': {'id': 1, 'driver': 'Sebastian Vettel', 'car': 'FERRARI', 'lap_time': '0:01:04.415000',
                              'abr': 'SVF'}}]


@pytest.fixture
def app():
    flask_app.config.from_object(Config)
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


def open_mock(filename):
    for expected_filename, content in FILES.items():
        if filename == expected_filename:
            return mock_open(read_data=content).return_value
    return MagicMock(side_effect=open_mock)


@pytest.fixture
def mocker_folder():
    file_mock = MagicMock()
    with mock.patch("builtins.open", open_mock(FILES)):
        yield file_mock


@pytest.fixture
def validate_path_db():
    with patch('web_report.db_manager.RacingDataAnalyzer.validate_path', return_value="path/to/open") as folder:
        yield folder


@pytest.fixture
def get_drivers():
    with patch('web_report.api_racer.api_views.RacersManager.get_drivers', return_value=FULL_DATA) as data:
        yield data


@pytest.fixture
def data_code():
    with patch('web_report.api_racer.api_views.RacersManager.data_code', return_value=FULL_DATA) as data:
        yield data


@pytest.fixture
def class_mock_db():
    with patch('web_report.db_manager.RacingDataAnalyzer') as MockClass:
        instance = MockClass.return_value
        instance.folder_path = 'test1'
        instance.data_folder = 'test2'
        yield MockClass


db = SqliteDatabase(':memory:')


@pytest.fixture
def use_db():
    db.bind([RaceResult], bind_refs=False, bind_backrefs=False)
    db.create_tables([RaceResult])
    yield db


@pytest.fixture
def empty_db():
    db.bind([RaceResult], bind_refs=False, bind_backrefs=False)
    yield db


@pytest.fixture()
def remove_db():
    yield
    db.drop_tables([RaceResult])
    db.close()


@pytest.fixture
def pop_db():
    for dr_info in DATA:
        RaceResult.create(
            driver=dr_info.driver,
            car=dr_info.car,
            lap_time=dr_info.lap_time,
            abr=dr_info.abr
        )
    yield RaceResult


@pytest.fixture
def class_mock():
    with patch.object(RacingDataAnalyzer, "__init__", lambda z, y: None):
        class_mock = RacingDataAnalyzer(PATH)
        class_mock.folder_path = PATH
        class_mock.data_folder = PATH
        yield class_mock
