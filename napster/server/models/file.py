class File(object):

    def __init__(self, name, hash, user):
        self._name = name
        self._hash = hash
        self._session_id = user.session_id

    def destroy(self):
        print "TODO"

    @property
    def name(self):
        return self._name

    @property
    def hash(self):
        return self._hash

    @property
    def session_id(self):
        return self._session_id
