from mongoengine import Document, StringField

class File(Document):
    name = StringField()
    hash = StringField()
    session_id = StringField(min_length = 16, max_length = 16)
