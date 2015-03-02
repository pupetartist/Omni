import webapp2

import models
import encoders
import util

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

application = webapp2.WSGIApplication([
    ('/?', Main),
    ('/route', Route)], debug=True)
