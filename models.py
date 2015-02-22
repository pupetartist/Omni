import security

from google.appengine.ext import ndb

class Account(ndb.Model):
    username = ndb.StringProperty(required = True)
    hashed_password = ndb.StringProperty(required = True)
    email = ndb.StringProperty()

    def is_valid_password(self, password):
        hashed_password, salt = self.hashed_password.split(',')
        computed_hashed_password = security.hash_password(password, salt)
        return self.hashed_password == computed_hashed_password

    def id(self):
        return self.key.id()

    @classmethod
    def by_username(cls, username):
        return cls.query(cls.username == username).get()

    @classmethod
    def register_account(cls, username, password, email):
        hashed_password = security.hash_password(password)
        account = Account(username = username, hashed_password = hashed_password, email = email)
        account.put()
        return account

    @classmethod
    def login(cls, username, password):
        if username and password:
            account = cls.by_username(username)
            if account and account.is_valid_password(password):
                return account
