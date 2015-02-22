import logging
import security
import cookies

from base import BaseHandler
from models import Account

class AuthenticatedHandler(BaseHandler):
    def initialize(self, *params, **named_params):
        BaseHandler.initialize(self, *params, **named_params)
        self.account = self.get_logged_in_account()

    def render(self, template_name, **named_params):
        account_username = self.account.username if self.account else None
        BaseHandler.render(self, template_name, account_username = account_username, **named_params)

    def auth_get(self, *params, **named_params):
        pass

    def auth_post(self, *params, **named_params):
        pass

    def not_authorized_exception(self):
        logging.info(self.request.headers)
        self.abort(401, headers = {'page_path' : self.request.path_qs})

    def not_found_exception(self):
        logging.info(self.request.headers)
        self.abort(404, headers = {'page_path' : self.request.path_qs})

    def get(self, *params, **named_params):        
        if self.is_logged_in():
            self.auth_get(*params, **named_params)
        else:
            self.not_authorized_exception()

    def post(self, *params, **named_params):
        if self.is_logged_in():
            self.auth_post(*params, **named_params)
        else:
            self.not_authorized_exception()

    def get_logged_in_account(self):
        account_id = self.get_session_id()
        if account_id:
            return Account.get_by_id(long(account_id))

    def is_logged_in(self):
        return self.account != None

    def account_exists(self, username):
        return Account.by_username(username) != None

    def get_session_id(self):
        account_id_cookie = self.request.cookies.get(cookies.USER_ID, None)
        if account_id_cookie:
            return security.get_secure_cookie_value(account_id_cookie)

    def establish_session(self, account):
        self.abandon_session()
        logging.info('Establishing session for user id: %s', account.id())
        self.account = account
        self.add_cookie(cookies.USER_ID, 
                        security.set_secure_cookie_value(str(account.id())))

    def abandon_session(self):
        if self.is_logged_in():
            self.account = None
            self.remove_cookie(cookies.USER_ID)

    def login(self, username, password):
        account = Account.login(username, password)
        if not account:
            return 'Invalid username or password'
        self.establish_session(account)
    
