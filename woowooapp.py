import cgi
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb
from webapp2_extras import json
import webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write('hello')

class Guestbook(webapp2.RequestHandler):
    def post(self):
        self.response.write('<html><body>You wrote:<pre>')
        self.response.write(cgi.escape(self.request.get('content')))
        self.response.write('</pre></body></html>')

class Start(webapp2.RequestHandler):
    def post(self):
        data = self.request.body
        parsed_json = json.decode(data)
        site = parsed_json['site']
        contact = parsed_json['contact']
        print site
        print contact

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', Guestbook),
    ('/update', Start),
], debug=True)
