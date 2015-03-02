import security
import db.null

from util import singleton


@singleton
class Persistence:
    engine = db.null

class Account:
    account = Persistence().engine.Account

    @classmethod
    def new(cls, username, password, email):
        hashed_password = security.hash_password(password)
        return cls.account.new(username=username,
                               hashed_password=hashed_password,
                               email=email)

    @classmethod
    def by_username(cls, username):
        return cls.account.by_username(username)

    @classmethod
    def by_id(cls, _id):
        return cls.account.by_id(_id)

    @classmethod
    def register_account(cls, username, password, email):
        hashed_password = security.hash_password(password)
        account = cls.new(username, hashed_password, email)
        return account.save()

    @classmethod
    def login(cls, username, password):
        if username and password:
            account = cls.by_username(username)
            if account and account.is_valid_password(password):
                return account
