import os
from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class Racer:
    lap_time: str
    car: str
    driver: str
    abr: str


class RacingDataAnalyzer:

    def __init__(self, path: str) -> None:
        self.data_folder = None
        self.folder_path = path
        self.racer_data = None
        self.racer_time = None
        self.start_list = None
        self.end_list = None
        self.abbreviations_list = None

    def validate_path(self) -> str:
        """Checks if the folder exists."""
        data_folder = os.path.join(os.path.abspath('.'), self.folder_path)
        if not os.path.isdir(data_folder):
            raise FileNotFoundError('Folder not found')
        self.data_folder = str(data_folder)
        return self.data_folder

    def read_files(self) -> List[List[str]]:
        """Read files from files and store in lists"""
        data_from_files = []
        files = ["start.log", "end.log", "abbreviations.txt"]
        for file in files:
            file = os.path.join(self.data_folder, file)
            with open(file) as file_:
                data_from_files.append([line for line in file_ if line.strip() != ""])
        self.start_list, self.end_list, self.abbreviations_list = data_from_files
        return [self.start_list, self.end_list, self.abbreviations_list]

    def build_report(self) -> List[Racer]:
        """
        Lap time calculation.
        :return:
            Data with lap time, car and driver name.
        """
        time_reg = '%H:%M:%S.%f'
        racer_data = []
        for start_item in self.start_list:
            end = str([end_time for end_time in self.end_list if (start_item[0:7] in end_time)])
            abbrev = [name.strip() for name in self.abbreviations_list if (start_item[0:3] in name)]
            lap_time = datetime.strptime(end[16:28], time_reg) - datetime.strptime(start_item[14:26], time_reg)
            if '-' not in str(lap_time):
                abr, driver, car = abbrev[0].split('_', 2)
                racer_data.append(Racer(str(lap_time), car, driver, abr))
        self.racer_data = racer_data
        return self.racer_data
