import webapp2

import models
import encoders
import util
import os

from base import BaseHandler


class Main(BaseHandler):
    def get(self):
        self.render('main.html')


class Route(BaseHandler):
    def get(self):
        origin = self.request.get('origin')
        destination = self.request.get('destination')
        self.render('route.html', origin=origin, destination=destination)


def select_persistence_engine():
    if util.on_gae_platform():
        import db.gae
        return db.gae
    import db.null
    return db.null


def select_encoder():
    if util.on_gae_platform():
        import encoders.gae
        return encoders.gae
    import encoders.null
    return encoders.null

# Select implementation-specific database and json encoding APIs
models.Persistence().engine = select_persistence_engine()
encoders.JsonEncoder().encoder = select_encoder()

routing = [
    (r'/?', Main),
    (r'/route', Route)
]

config = {}

if not util.on_gae_platform():
    import webapp2_static
    routing.insert(0, (r'/static/(.+)', webapp2_static.StaticFileHandler))
    config.update({'webapp2_static.static_file_path': 'static/'})
    
application = webapp2.WSGIApplication(routing, config=config, debug=True)

# This is just to support running out of GAE
# Inside GAE, static routes are specified in the yaml file
def main():
    from paste import httpserver
    port = os.getenv('VCAP_APP_PORT', 11080)
    host = os.getenv('VCAP_APP_HOST', 'localhost')
    httpserver.serve(application, host=host, port=port)

if __name__ == '__main__':
    if not util.on_gae_platform():
        main()
