__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

from mongoengine import *


class User(Document):
    ip = StringField()
    port = IntField()
    session_id = StringField(min_length = 16, max_length = 16)