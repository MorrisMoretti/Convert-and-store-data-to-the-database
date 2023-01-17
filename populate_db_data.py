import argparse

from config import DB
from web_report import logging
from web_report.db_manager import init_db, insert_to_db, read_files


def run_parser() -> argparse.Namespace:
    """Run parser with arguments"""
    parser = argparse.ArgumentParser(description="Race statistics")
    parser.add_argument('--files', dest="folder", help="File folder")
    return parser.parse_args()


def main() -> None:
    args = run_parser()
    if args.folder is None:
        raise ValueError('Please select --files dir')
    racer_data = read_files(args.folder)
    init_db(DB)
    insert_to_db(racer_data=racer_data)
    logging.info('Successful db create')


if __name__ == '__main__':
    main()
