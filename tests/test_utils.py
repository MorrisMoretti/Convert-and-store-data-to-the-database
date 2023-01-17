import os
from unittest.mock import patch

import pytest

from tests.conftest import DATA, FILES, PATH
from web_report import RacingDataAnalyzer


def test_init():
    class_mock = RacingDataAnalyzer(PATH)
    assert class_mock.folder_path == PATH


@patch('os.path.isdir')
def test_validate_path(mock_isdir, class_mock):
    assert os.path.join(os.path.abspath('.'), PATH) == class_mock.validate_path()
    mock_isdir.assert_called_once()


def test_validate_path_err(class_mock):
    with pytest.raises(FileNotFoundError) as exc:
        class_mock.validate_path()
    assert "Folder not found" in str(exc.value)


def test_read_files(class_mock, mocker_folder):
    class_mock.data_folder = PATH
    assert class_mock.read_files() == [[item] for item in FILES.values()]


def test_build_report(class_mock):
    class_mock.start_list, class_mock.end_list, class_mock.abbreviations_list = [[item] for item in FILES.values()]
    assert class_mock.build_report() == [next(iter(DATA))]
