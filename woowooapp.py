import cgi
import urllib

from datetime import date, timedelta

from google.appengine.api import users, mail
from google.appengine.ext import ndb
from webapp2_extras import json, routes
import webapp2

class Site(ndb.Model):
    """Models a site with a site name, closing date, address"""
    name = ndb.StringProperty()
    location = ndb.GeoPtProperty()
    address_one = ndb.StringProperty()
    address_two = ndb.StringProperty()
    postcode = ndb.StringProperty()

class Contact(ndb.Model):
    """Models a contact of the site with a name, email and phone numbers"""
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    phone = ndb.StringProperty()
    mobile = ndb.StringProperty()

class Installation(ndb.Model):
    """Models an installation with a date set on creation, installation date,
    delivery date and pickup date, booleans to monitor stages of confirmations for
    contractot, haulier, customer and retailer and associated sites and contacts.
    """
    created_date = ndb.DateProperty(auto_now_add=True)
    installation_date = ndb.DateProperty()
    delivery_date = ndb.DateProperty()
    pickup_date = ndb.DateProperty()
    contractor_confirmed = ndb.BooleanProperty(default=False)
    haulier_confirmed = ndb.BooleanProperty(default=False)
    customer_confirmed = ndb.BooleanProperty(default=False)
    retailer_confirmed = ndb.BooleanProperty(default=False)
    sites = ndb.StructuredProperty(Site, repeated=True)
    contacts = ndb.StructuredProperty(Contact, repeated=True)

    @classmethod
    def query_installtion(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key).order(-cls.created_date)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('<html><body>')
        installations = Installation.query().fetch(20)

        for installation in installations:
            self.response.out.write('<blockquote>%s</blockquote>' %
                                    cgi.escape(installation.sites[0].name))
        self.response.out.write('</body></html>'
                )

class InstallationHandler(webapp2.RequestHandler):
    def get(self, installation_id):
        self.response.out.write('<html><body><h4>This is the installtion %s</h4>'
                % installation_id)
        self.response.out.write('</body></html>')

class InstallationListHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('<html><body><h4>A list of all the installations:</h4><ul>')
        installations = Installation.query().fetch(20)

        for installation in installations:
            self.response.out.write('<li>%s</li>' %
                                    cgi.escape(installation.sites[0].name))
        self.response.out.write('</ul></body></html>')

class InstallationAdditionHandler(webapp2.RequestHandler):
    def post(self):
        def next_weekday(d, weekday):
            days_ahead = weekday - d.weekday()
            if days_ahead <= 0: # Target day already happened this week
                days_ahead += 7
            return d + timedelta(days_ahead)
        base_url = "http://0.0.0.0:8080/"
        installation = Installation(
                id=self.request.POST['site-name'],
                sites=[Site(name = self.request.POST['site-name'],
                            address_one = self.request.POST['site-add-one'],
                            address_two = self.request.POST['site-add-two'],
                            postcode = self.request.POST['site-postcode'])],
                contacts=[Contact(name=self.request.POST['contact-firstname'] + " " + self.request.POST['contact-lastname'],
                            email = self.request.POST['contact-email'],
                            phone = self.request.POST['contact-landline'],
                            mobile = self.request.POST['contact-mobile'])]
        )
        installation_key = installation.put()
        print installation_key
        provisional_date = installation.created_date
        print "date created: ", provisional_date
        prov_date_buffer = timedelta(days=42)
        provisional_date += prov_date_buffer
        provisional_date = next_weekday(provisional_date, 0)
        print "next monday from date: ", provisional_date
        yes_link = base_url +  "/yes"
        no_link = base_url, "/no"
        print "provisional date: ", provisional_date, " (add 6 weeks)"
        mail.send_mail(sender="WooWoo Waterless Toilets <joel.greta@gmail.com>",
                to="Joel <joel@joelcormack.com>",
                subject="Please confirm this provisional date",
                body="""
Hi Jake,

An order has come through for a toilet installation, could you please confirm that the week beginning %s is ok for you for an installation?

Please confirm by clicking the below link.

<a href="%s">YES</a>

otherwise to choose another week click the following link.

<a hfre="%s">NO</a>

""" % (provisional_date, yes_link, no_link) )

class InstallationStatusHandler(webapp2.RequestHandler):
    def get(self, installation_id, status):
        self.response.out.write('<html><body><h4>This is the installtion %s and this is the status %s</h4>'
                % (installation_id, status))
        self.response.out.write('</body></html>')


app = webapp2.WSGIApplication([
    webapp2.Route(r'/', MainPage),
    routes.PathPrefixRoute('/installations', [
        webapp2.Route('/', handler=InstallationListHandler, name='installation-list'),
        webapp2.Route('/add', handler=InstallationAdditionHandler),
        webapp2.Route('/<installation_id>', handler=InstallationHandler),
        webapp2.Route('/<installation_id>/<status>', handler=InstallationStatusHandler),
    ]),
], debug=True)
