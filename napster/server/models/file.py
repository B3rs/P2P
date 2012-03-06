class File:

    def __init__(self, name, hash, user):
        self.name = name
        self.hash = hash
        self.session_id = user.session_id


