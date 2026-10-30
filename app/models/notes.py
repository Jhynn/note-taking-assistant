import datetime

from peewee import Model, CharField, TextField, DateTimeField
from app.core.database import db


class Note(Model):
    id: int
    title = CharField(max_length=256)
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db
        table_name = 'notes'
