import os
import mimetypes
import webapp2
import logging


class StaticFileHandler(webapp2.RequestHandler):
    def get(self, path):
        abs_path = os.path.abspath(
            os.path.join(
                self.app.config.get('webapp2_static.static_file_path', 'static'),
                path))
        if os.path.isdir(abs_path) or abs_path.find(os.getcwd()) != 0:
            self.response.set_status(403)
            return
        try:
            with open(abs_path, 'rb') as f:
                self.response.headers['Content-Type'] = mimetypes.guess_type(abs_path)[0]
                # webapp2 seems to try to guess the size of the content, but it fails to do it
                # correctly (at least in Windows) on its own, so we'll give it a little help
                file_bytes = f.read()
                self.response.headers['Content-Length'] = len(file_bytes)
                self.response.out.write(file_bytes)
        except:
            self.response.set_status(404)
