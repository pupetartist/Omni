from util import singleton
from . import AccountBase

@singleton
class Account(AccountBase):
    def __init__(self):
        pass

    def get_username(self): pass
    def set_username(self): pass
    username = property(get_username, set_username)

    def get_hashed_password(self): pass
    def set_hashed_password(self): pass
    hashed_password = property(get_hashed_password, set_hashed_password)

    def get_email(self): pass
    def set_email(self): pass
    email = property(get_email, set_email)

    @classmethod
    def new(cls, username, hashed_password, email):
        return Account()

    @classmethod
    def by_username(cls, username):
        return Account()

    @classmethod
    def by_id(cls, _id):
        return Account()

    def id(self):
        return 0

    def save(self):
        return True
