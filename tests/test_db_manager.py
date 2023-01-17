from tests.conftest import DATA, DATA_VALUE
from web_report.db_manager import init_db, insert_to_db, read_files


def test_read_files(class_mock_db, validate_path_db):
    assert 'RacingDataAnalyzer().build_report()' in str(read_files(folder="path/to/open"))


def test_insert_to_dp(use_db, remove_db):
    data_db = insert_to_db(DATA)
    assert [data_db.lap_time, data_db.car, data_db.driver, data_db.abr] == DATA_VALUE


def test_init_db(empty_db, remove_db):
    init_db(empty_db)
    assert empty_db.get_tables() == ['RaceResult']
