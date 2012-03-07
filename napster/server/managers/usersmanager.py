from models.user import User

class UserManager:

    @classmethod
    def find_user_by_session_id(cls, session_id):
        print "TODO: Find user from session_id: "+session_id
        return null

    @classmethod
    def create_user(cls, ip, port):
        user = User(ip, port)
        #todo: save user

    @classmethod
    def delete_user(cls, user):
        user.destroy()
        #todo delete user from db
