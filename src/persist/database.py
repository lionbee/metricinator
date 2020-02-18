"""
ORM for persisting metrics
"""
import datetime
from peewee import (
    Database,
    DatabaseProxy,
    CharField,
    DateTimeField,
    FloatField,
    ForeignKeyField,
    Model,
)

database_proxy = DatabaseProxy()


def set_database(db: Database):
    database_proxy.initialize(db)
    db.create_tables([Host, Metric, Gauge])


class BaseModel(Model):
    class Meta:
        database = database_proxy


class Host(BaseModel):
    name = CharField(unique=True)


class Metric(BaseModel):
    name = CharField(unique=True)


class Gauge(BaseModel):
    host = ForeignKeyField(Host, backref="gauges")
    metric = ForeignKeyField(Metric, backref="gauges")
    created_date = DateTimeField(default=datetime.datetime.now)
    measure = FloatField()
