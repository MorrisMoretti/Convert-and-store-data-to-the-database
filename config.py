import os

import peewee

DB = peewee.SqliteDatabase('race_result.db')


class Config:
    JSON_SORT_KEYS = os.getenv("JSON_SORT_KEYS", False)
    JSON_AS_ASCII = os.getenv("JSON_AS_ASCII", False)
    DEBUG = os.getenv("DEBUG", True)
