# main.py

from google.appengine.ext import webapp
from google.appengine.ext.webapp import RequestHandler
from google.appengine.ext.webapp.util import run_wsgi_app
from simple_login import SimpleLoginHandler
from acct_lookup import AcctLookupHandler

class RedirectToHomeHandler(RequestHandler):
	def get(self):
		self.redirect('/static/home.html')
	
#
# Main:
#
application = webapp.WSGIApplication([('/', RedirectToHomeHandler),
                                      ('/login', SimpleLoginHandler),
                                      ('/accountLookup', AcctLookupHandler)],
                                      debug=True)
run_wsgi_app(application)