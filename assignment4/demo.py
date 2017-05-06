from google.appengine.ext import ndb
import logging
import webapp2
import json

class OauthHandler(webapp2.RequestHandler):
  def get(self):
    get1 = repr(self.request.GET);
    logging.debug('The contents of the GET request are:' + get1)

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.write("hello");
    	#self.response.write(get1)
		
app = webapp2.WSGIApplication([
	('/', MainPage),
	('/oauth', OauthHandler)
], debug=True)