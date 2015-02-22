import random
import hashlib
import hmac
import string
import config_devel

def hash_value(value, salt):
    # Python's HMAC does NOT accept unicode
    value = str(value) if type(value) is unicode else value
    salt = str(salt) if type(salt) is unicode else salt

    return hmac.new(salt, value, hashlib.sha256).hexdigest()

def make_salt(length=5):
    return ''.join(random.choice(string.letters) for x in range(length))

def hash_password(password, salt=None):
    if not salt:
        salt = make_salt()
    return '%s,%s' % (hash_value(password, salt), salt)

def set_secure_cookie_value(cookie_value):
    return '%s|%s' % (cookie_value, hash_value(cookie_value, config_devel.PASSWORD_SECRET))

def get_secure_cookie_value(safe_cookie_value):
    cookie_value = safe_cookie_value.split('|')
    if len(cookie_value) > 1 and set_secure_cookie_value(cookie_value[0]) == safe_cookie_value:
        return cookie_value[0]
