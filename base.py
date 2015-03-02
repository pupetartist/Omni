import webapp2
import os
import logging
import json

import util

from jinja2 import Environment, FileSystemLoader
from jinja2.filters import do_capitalize, do_truncate

import datetime_format
import encoders

templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = Environment(loader=FileSystemLoader(templates_dir), autoescape=True)
jinja_env.filters['do_capitalize'] = do_capitalize
jinja_env.filters['do_truncate'] = do_truncate
jinja_env.filters['datetime'] = datetime_format.simple_datetime

class BaseHandler(webapp2.RequestHandler):
    def initialize(self, *params, **named_params):
        webapp2.RequestHandler.initialize(self, *params, **named_params)
        self.ROOT_PATH = '/'

    def handle_exception(self, exception, debug):
        logging.exception(exception)

        if isinstance(exception, webapp2.HTTPException):
            logging.error(exception.headers)
            self.render(str(exception.code), page_path = exception.headers['page_path'])
            self.response.set_status(exception.code)
        else:
            self.response.set_status(500)

    def write(self, content):
        self.response.write(content)

    def render(self, template_name, **keywords):
        template_name = util.ensure_extension(template_name, 'html')
        template = jinja_env.get_template(template_name)
        self.write(template.render(**keywords))

    def add_cookie(self, name, value):
        self.response.headers.add_header('Set-Cookie', '%s=%s;Path=/' % (name, value))

    def remove_cookie(self, name):
        self.add_cookie(name, '')

    def send_as_json(self, obj):
        self.response.headers['Content-Type'] = 'application/json;charset=UTF-8'
        self.write(json.dumps(obj, cls=encoders.JsonEncoder.encoder))
