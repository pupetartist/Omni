import webapp2
from base import BaseHandler

class Main(BaseHandler):
    def get(self):
        self.render('main.html')

class Route(BaseHandler):
    def get(self):
        origin = self.request.get('origin')
        destination = self.request.get('destination')
        self.render('route.html', origin=origin, destination=destination)

application = webapp2.WSGIApplication([
    ('/?', Main),
    ('/route', Route)], debug=True)
