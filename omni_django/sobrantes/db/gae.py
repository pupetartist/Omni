from google.appengine.ext import ndb
from . import AccountBase
import noconflict

class Account(ndb.Model, AccountBase):
    # If you get an error along the lines of:
    # >> metaclass conflict: the metaclass of a derived class must be a
    # >> (non-strict) subclass of the metaclasses of all its bases
    # you'll need the following line.
    # For more details see the "noconflict" module
    __metaclass__ = noconflict.classmaker()

    username = ndb.StringProperty(required=True)
    hashed_password = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)

    @classmethod
    def new(cls, username, hashed_password, email):
        return cls(
            username=username, hashed_password=hashed_password, email=email)

    @classmethod
    def by_username(cls, username):
        return cls.query(cls.username == username).get()

    @classmethod
    def by_id(cls, _id):
        return cls.get_by_id(_id)

    def id(self):
        return self.key.id()

    def save(self):
        return self.put()

