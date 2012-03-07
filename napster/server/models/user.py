from mongoengine import *

class User(Document):
    ip = StringField() #TODO make specs complaint
    port = IntField() #TODO make specs complaint
    session_id = StringField(min_length = 10, max_length = 10)