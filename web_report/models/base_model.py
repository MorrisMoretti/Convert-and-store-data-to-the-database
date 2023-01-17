import peewee

from config import DB


class BaseModel(peewee.Model):
    class Meta:
        database = DB
        encodings = 'utf.8'
