"""lib.models model classies"""

from peewee import *
import config as cfg

database = SqliteDatabase(cfg.database)

class BaseModel(Model):
    class Meta:
        database = database

class Question(BaseModel):
    content = TextField()
    image = CharField()
    #code = FixedCharField(max_length=32, default=None)
    class Meta:
        auto_increment = True

class Choice(BaseModel):
    question = ForeignKeyField(Question)
    content = TextField()
    status = IntegerField(default=0)
    #code = FixedCharField(max_length=32, default=None)
    class Meta:
        auto_increment = True

class User(BaseModel):
    username = CharField()
    password = CharField()
    email = CharField()
    join_date = DateTimeField()

