import logging
from typing import List

from web_report.models.race_model import RaceResult
from web_report.utils import Racer, RacingDataAnalyzer


def read_files(folder: str) -> List[Racer]:
    analyzer = RacingDataAnalyzer(folder)
    analyzer.validate_path()
    logging.info('Successful validate_path ')
    analyzer.read_files()
    logging.info('Successful read from files ')
    return analyzer.build_report()


def init_db(db):
    db.create_tables([RaceResult])


def insert_to_db(racer_data: List[Racer]):
    for dr_info in racer_data:
        RaceResult.create(
            driver=dr_info.driver,
            car=dr_info.car,
            lap_time=dr_info.lap_time,
            abr=dr_info.abr
        )
    logging.info('Successful insert to db ')
    return RaceResult
