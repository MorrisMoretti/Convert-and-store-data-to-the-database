from typing import Any, Dict, List

from web_report.models import RaceResult


def driver_enum(racer_data: [Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [{'position': num, 'driver_info': inf} for num, inf in racer_data]


class RacersManager:

    @staticmethod
    def get_drivers(direction: str) -> List[Any]:
        drivers = RaceResult().select().dicts().order_by(RaceResult.lap_time.asc())
        if direction == 'desc':
            return driver_enum(reversed(list(enumerate(drivers, start=1))))
        return driver_enum(enumerate(drivers, start=1))

    @staticmethod
    def data_code(code: str) -> List[Dict[str, Any]]:
        return [{'driver_info': inf} for inf in RaceResult().select().dicts().where(RaceResult.abr == code)]
