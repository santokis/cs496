<<<<<<< HEAD
import webapp2
import urllib
import urlparse
import json
import os
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import template

#url message set variables
responseType = 'code'
clientId = '591609081019-4q3oniuktljmlbendk3p8823fg3o2i09.apps.googleusercontent.com'
clientSecret = 'IB-XtHpsM148zLGHq8KGPfN6'
redirectUri = 'https://assignment4-166505.appspot.com/oauth'
scope = 'email'
state = 'assignment4oauth2'
grantType = 'authorization_code'
authPath = 'https://accounts.google.com/o/oauth2/v2/auth'
tokenUrl = 'https://www.googleapis.com/oauth2/v4/token'
infoUrl = 'https://www.googleapis.com/plus/v1/people/me'
homeUrl = 'https://assignment4-166505.appspot.com'

class OAuthHandler(webapp2.RequestHandler):
	def get(self):
		#get state and code from returned url
		url = self.request.url
		parsed = urlparse.urlparse(url)
		newState = self.request.get("state")
		code = self.request.get("code")
		
		#####DEBUG#####
		#self.response.write(url)
		#self.response.write(parsed)
		#self.response.write(newState)
		#self.response.write(code)

		#verify state matches one previous state sent
		if state == newState:
			pass
		else:
			self.redirect(homeUrl)

		#send post request to oauth server with code
		data = {'code':code,'client_id':clientId,'client_secret':clientSecret,'redirect_uri':redirectUri,'grant_type':grantType}
		encoded = urllib.urlencode(data)
		result = urlfetch.fetch(url=tokenUrl, payload=encoded, method=urlfetch.POST)
		resultData = json.loads(result.content)
		token = resultData['access_token']

		#####DEBUG#####
		#self.response.write(result.content)
		#self.response.write(token)

		#final GET request to oauth server with token
		head = {'Authorization':'Bearer ' + token}
		result = urlfetch.fetch(url=infoUrl, headers=head, method='GET')
		resultData = json.loads(result.content)
		gPlusUser = resultData['isPlusUser']

		#error handling if user does not have a google+ profile
		if gPlusUser:
			userName = resultData['displayName']
			userUrl = resultData['url']
			#http://webapp2.readthedocs.io/en/latest/tutorials/gettingstarted/templates.html
			template_values = {'userName':userName,'userUrl':userUrl,'userVar':code}
			path = os.path.join(os.path.dirname(__file__), 'main.html')
			self.response.out.write(template.render(path, template_values))

			#####DEBUG#####
			#self.response.write(result.content)
			#self.response.write(userName)
			#self.response.write(userUrl)
		else:
			template_values = {}
			path = os.path.join(os.path.dirname(__file__), 'error.html')
			self.response.out.write(template.render(path, template_values))

class LoginPage(webapp2.RequestHandler):
	def get(self):
		#direct end user to oauth server via GET request
		authUrl = authPath+'?response_type='+responseType+'&client_id='+clientId+'&redirect_uri='+redirectUri+'&scope='+scope+'&state='+state
		head = {'Content-Type':'text/plain'}
		result = urlfetch.fetch(url=authUrl, headers=head, method='GET')
		self.response.write(result.content)

class MainPage(webapp2.RequestHandler):
	def get(self):
		#http://webapp2.readthedocs.io/en/latest/tutorials/gettingstarted/templates.html
		template_values = {}
		path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/login', LoginPage),
  ('/oauth', OAuthHandler)
=======
import webapp2
import urllib
import urlparse
import json
import os
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import template

#url message set variables
responseType = 'code'
clientId = '591609081019-4q3oniuktljmlbendk3p8823fg3o2i09.apps.googleusercontent.com'
clientSecret = 'IB-XtHpsM148zLGHq8KGPfN6'
redirectUri = 'https://assignment4-166505.appspot.com/oauth'
scope = 'email'
state = 'assignment4oauth2'
grantType = 'authorization_code'
authPath = 'https://accounts.google.com/o/oauth2/v2/auth'
tokenUrl = 'https://www.googleapis.com/oauth2/v4/token'
infoUrl = 'https://www.googleapis.com/plus/v1/people/me'
homeUrl = 'https://assignment4-166505.appspot.com'

class OAuthHandler(webapp2.RequestHandler):
	def get(self):
		#get state and code from returned url
		url = self.request.url
		parsed = urlparse.urlparse(url)
		newState = self.request.get("state")
		code = self.request.get("code")
		
		#####DEBUG#####
		#self.response.write(url)
		#self.response.write(parsed)
		#self.response.write(newState)
		#self.response.write(code)

		#verify state matches one previous state sent
		if state == newState:
			pass
		else:
			self.redirect(homeUrl)

		#send post request to oauth server with code
		data = {'code':code,'client_id':clientId,'client_secret':clientSecret,'redirect_uri':redirectUri,'grant_type':grantType}
		encoded = urllib.urlencode(data)
		result = urlfetch.fetch(url=tokenUrl, payload=encoded, method=urlfetch.POST)
		resultData = json.loads(result.content)
		token = resultData['access_token']

		#####DEBUG#####
		#self.response.write(result.content)
		#self.response.write(token)

		#final GET request to oauth server with token
		head = {'Authorization':'Bearer ' + token}
		result = urlfetch.fetch(url=infoUrl, headers=head, method='GET')
		resultData = json.loads(result.content)
		gPlusUser = resultData['isPlusUser']

		#error handling if user does not have a google+ profile
		if gPlusUser:
			userName = resultData['displayName']
			userUrl = resultData['url']
			#http://webapp2.readthedocs.io/en/latest/tutorials/gettingstarted/templates.html
			template_values = {'userName':userName,'userUrl':userUrl,'userVar':code}
			path = os.path.join(os.path.dirname(__file__), 'main.html')
			self.response.out.write(template.render(path, template_values))

			#####DEBUG#####
			#self.response.write(result.content)
			#self.response.write(userName)
			#self.response.write(userUrl)
		else:
			template_values = {}
			path = os.path.join(os.path.dirname(__file__), 'error.html')
			self.response.out.write(template.render(path, template_values))

class LoginPage(webapp2.RequestHandler):
	def get(self):
		#direct end user to oauth server via GET request
		authUrl = authPath+'?response_type='+responseType+'&client_id='+clientId+'&redirect_uri='+redirectUri+'&scope='+scope+'&state='+state
		head = {'Content-Type':'text/plain'}
		result = urlfetch.fetch(url=authUrl, headers=head, method='GET')
		self.response.write(result.content)

class MainPage(webapp2.RequestHandler):
	def get(self):
		#http://webapp2.readthedocs.io/en/latest/tutorials/gettingstarted/templates.html
		template_values = {}
		path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/login', LoginPage),
  ('/oauth', OAuthHandler)
>>>>>>> ac6e1a7f65e0bfc328feb4a996db4038cdf2587a
], debug=True)