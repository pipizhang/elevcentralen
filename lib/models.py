import os
from peewee import *
from . import config as cfg

db = SqliteDatabase(cfg.get("database"))

class BaseModel(Model):
    class Meta:
        database = db

class Question(BaseModel):
    content = TextField()
    image = CharField()
    code = FixedCharField(max_length=32, default=None)
    is_known = BooleanField(default=False)
    class Meta:
        auto_increment = True

class Choice(BaseModel):
    question = ForeignKeyField(Question)
    content = TextField()
    status = IntegerField(default=0)
    code = FixedCharField(max_length=32, default=None)
    class Meta:
        auto_increment = True

class User(BaseModel):
    username = CharField()
    password = CharField()
    email = CharField()
    join_date = DateTimeField()

def setup(force = False):
    if force and os.path.isfile(cfg.get("database")):
        os.remove(cfg.get("database"))

    db.connect()
    db.create_tables([Question, Choice, User])

