import app.security
import abc

# abstractclassmethod is only available from abc only in Python 3
from app.util import abstractclassmethod

# This class is meant to be an abstract class (no fields should be added here)
class AccountBase:
    __metaclass__ = abc.ABCMeta

    def get_username(self): pass
    def set_username(self): pass
    username = abc.abstractproperty(get_username, set_username)

    def get_hashed_password(self): pass
    def set_hashed_password(self): pass
    hashed_password = abc.abstractproperty(get_hashed_password, set_hashed_password)

    def get_email(self): pass
    def set_email(self): pass
    email = abc.abstractproperty(get_email, set_email)


    # Hashed passwords are stored as: "hash,salt"
    def is_valid_password(self, password):
        hashed_password, salt = self.hashed_password.split(',')
        computed_hashed_password = security.hash_password(password, salt)
        return self.hashed_password == computed_hashed_password

    #
    # To be implemented by concrete classes
    #
    @abstractclassmethod
    def new(username, hashed_password, email):
        """Return an instance of the specific Account object"""
        pass

    @abstractclassmethod
    def by_username(cls, username):
        """Return an Account object matching USERNAME or None if there is none"""
        pass

    @abstractclassmethod
    def by_id(cls, _id):
        """Return an Account object matching _ID or None if there is none"""
        pass

    @abc.abstractmethod
    def id(self):
        """Returns a unique identifier for the account"""
        pass

    @abc.abstractmethod
    def save(self):
        """Synchronously commit the data in the object to the underlying data store.
        Returns True if the operation succeeded, False otherwise.
        """
        pass

