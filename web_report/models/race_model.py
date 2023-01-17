import peewee

from .base_model import BaseModel


class RaceResult(BaseModel):
    driver = peewee.TextField()
    car = peewee.TextField()
    lap_time = peewee.DateTimeField()
    abr = peewee.TextField()

    class Meta:
        db_table = 'RaceResult'
