__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

from mongoengine import Document, StringField, IntField

class File(Document):
    name = StringField()
    hash = StringField()
    session_id = StringField(min_length = 16, max_length = 16)
    download_count = IntField(default=0)
