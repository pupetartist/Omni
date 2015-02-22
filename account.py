import cgi
import logging

from authenticated import AuthenticatedHandler
from models import Account

class Login(AuthenticatedHandler):
    def initialize(self, *params, **named_params):
        AuthenticatedHandler.initialize(self, *params, **named_params)

    def render_form(self, redirect_url, login_error=''):
        self.render('login', redirect_url = redirect_url, login_error = login_error)

    def get(self):
        if self.is_logged_in():
            self.redirect(self.ROOT_PATH)
        else:
            redirect_url = self.request.get('redirect_url', self.ROOT_PATH)
            self.render_form(redirect_url)

    def post(self):
        if self.is_logged_in():
            self.redirect_url(self.ROOT_PATH)
            return

        redirect_url = self.request.get('redirect_url', self.ROOT_PATH)
        username = self.request.get('username')
        password = self.request.get('password')
        login_error = self.login(username, password)

        if login_error:
            self.render_form(redirect_url, login_error = login_error)
        else:
            logging.info('Redirecting to %s' % redirect_url)
            self.redirect(redirect_url)

class Logout(AuthenticatedHandler):
    def auth_get(self):
        self.auth_post()

    def auth_post(self):
        redirect_url = self.request.get('redirect_url', self.ROOT_PATH)
        self.abandon_session()
        self.redirect(redirect_url)

import re
class Signup(AuthenticatedHandler):
    def initialize(self, *params, **named_params):
        AuthenticatedHandler.initialize(self, *params, **named_params)
        self.USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        self.PASSWORD_RE = re.compile(r"^.{3,20}$")
        self.EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

    def get(self):
        if self.is_logged_in():
            self.redirect(self.ROOT_PATH)
        else:
            redirect_url = self.request.get('redirect_url', self.ROOT_PATH)
            self.render_form(redirect_url = redirect_url)

    def post(self):
        if self.is_logged_in():
            self.redirect(self.ROOT_PATH)
            return

        redirect_url = self.request.get('redirect_url', self.ROOT_PATH)
        user_username = self.request.get('username')
        user_password = self.request.get('password')
        user_verify = self.request.get('verify')
        user_email = self.request.get('email')

        username_error = self.validate_username(user_username)
        password_error, verify_error = self.validate_password(user_password, user_verify)
        email_error = self.validate_email(user_email)
        
        if username_error or password_error or verify_error or email_error:
            self.render_form(redirect_url, user_username, user_email, 
                            username_error, password_error, verify_error, email_error)
        else:
            account = Account.register_account(user_username, user_password, user_email)
            self.establish_session(account)
            self.redirect(redirect_url)

    def validate_username(self, user_username):
        if not self.USER_RE.match(user_username):
            return "That's not a valid username."
        if self.account_exists(user_username):
            return "That user already exists."

    def validate_password(self, user_password, user_verify):
        if not self.PASSWORD_RE.match(user_password):
            return "That wasn't a valid password.", None
        if user_password <> user_verify:
            return None, "Your passwords didn't match."
        return None, None

    def validate_email(self, user_email):
        if user_email and not self.EMAIL_RE.match(user_email):
            return "That's not a valid email."
            
    def render_form(self, redirect_url='', username='', email='',
                   username_error=None, password_error=None, verify_error=None, email_error=None):
        self.render('signup', 
                    redirect_url = redirect_url,
                    username = cgi.escape(username),
                    email = cgi.escape(email),
                    username_error = username_error or '',
                    password_error = password_error or '',
                    verify_error = verify_error or '',
                    email_error = email_error or '')

