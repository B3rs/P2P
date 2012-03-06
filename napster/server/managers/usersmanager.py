from napster.server.models.user import User

class UserManager:

    @classmethod
    def find_by_session_id(cls, session_id):
        print "Find user from session_id: "+session_id
        return null

    @classmethod
    def create_user(cls, ip, port):
        u = User(ip, port)
