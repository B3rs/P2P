from mongoengine import Document, StringField

class File(Document):
    name = StringField()
    hash = StringField()
    session_id = StringField(min_length = 10, max_length = 10)
