import argparse
import logging
from argparse import Namespace
from unittest import mock
from unittest.mock import patch

import pytest

from populate_db_data import main, run_parser
from tests.conftest import DATA, DRIVER1
from web_report import RaceResult


@mock.patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(folder='road_data'))
def test_run_parser(mock_args):
    assert run_parser() == Namespace(folder='road_data')
    mock_args.assert_called()


@patch('populate_db_data.run_parser', return_value=Namespace(folder='road_data'))
@patch('populate_db_data.read_files', return_value=DATA)
def test_main(mock_run_parser, mock_read_files, caplog, use_db, remove_db):
    create = RaceResult.create(driver=DRIVER1.driver, car=DRIVER1.car, lap_time=DRIVER1.lap_time, abr=DRIVER1.abr)
    with patch('populate_db_data.insert_to_db', return_value=create):
        caplog.set_level(logging.INFO)
        main()
        assert 'Successful db create' in caplog.text
    mock_run_parser.assert_called()
    mock_read_files.assert_called()


@patch('populate_db_data.run_parser', return_value=Namespace(folder=None))
def test_main_empty(mock_run_parser):
    with pytest.raises(ValueError):
        assert ValueError('Please select --file dir') == main()
    mock_run_parser.assert_called_once()
