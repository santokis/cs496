from google.appengine.ext import ndb
import webapp2
#https://docs.python.org/2/library/json.html
import json

class Boat(ndb.Model):
	id = ndb.StringProperty() #auto generated by API
	name = ndb.StringProperty() #name of the boat
	type = ndb.StringProperty() #type of the boat
	length = ndb.IntegerProperty() #length of the boat
	at_sea = ndb.BooleanProperty(default=True) #boolean indicating if boat is at sea
	
class BoatHandler(webapp2.RequestHandler):
	def post(self): #create boat
		parent_key = ndb.Key(Boat, "Fleet") #adding new boat to "Fleet"
		boat_data = json.loads(self.request.body) #new boat data being entered
		new_boat = Boat(name=boat_data['name'], type=boat_data['type'], length=boat_data['length'], parent=parent_key) #receiving data from body
		new_boat.put()
		new_boat.id = new_boat.key.urlsafe()
		new_boat.put()
		boat_dict = new_boat.to_dict()
		boat_dict['self'] = '/boat/' + new_boat.key.urlsafe()
		self.response.write(json.dumps(boat_dict))
	
	def get(self, id=None): #view boat(s)
		if id: #return a single boat
			boat = ndb.Key(urlsafe=id).get() #return the entity associated with boat
			self.response.write(boat)
		else: #return all boats
			all_boats = Boat.query().fetch()
			for b in all_boats:
				boat_dict = b.to_dict()
				self.response.write('\n')
				boat_dict['boat_url'] = '/boat/' + b.id #boat url requirement
				self.response.write(json.dumps(boat_dict))
	
	def delete(self, id): #delete boat
		try: #get "at_sea" value
			boat = ndb.Key(urlsafe=id).get()
			at_sea = boat.at_sea
			self.response.write(boat)
			self.response.write('\n')
			if at_sea == False: #not at sea, query slips for boat id and set to empty
				slip = Slip.query(Slip.current_boat == boat.id).get()
				slip.current_boat = ''
				slip.arrival_date = ''
				slip.put()
				self.response.write(slip)
				self.response.write('\n')
			boat.key.delete()
			self.response.write('Boat deleted successfully!')
		except:
			all_boats = Boat.query().fetch()
			if len(all_boats) < 1: #results returned for boats
				self.response.set_status(404) #resource not found
				self.response.write('No boats available.')
			else:
				for b in all_boats:
					self.response.write(b)
					self.response.write('\n')
				self.response.set_status(404) #resource not found
				self.response.write('Enter boat id in URL (example: /boat/{id} to delete)')
	
	def put(self, id): #assign boat to sea
		try:
			boat = ndb.Key(urlsafe=id).get() #holds current slip
			at_sea = boat.at_sea
			if at_sea:
				self.response.write('Boat is already at sea.')
			else:
				boat.at_sea = True
				boat.put()
				slip = Slip.query(Slip.current_boat == boat.id).get()
				slip.current_boat = ''
				slip.arrival_date = ''
				slip.put()
				self.response.write(boat)
				self.response.write('\n')
				self.response.write(slip)
		except:
			all_boats = Boat.query().fetch()
			if len(all_boats) < 1: #results returned for boats
				self.response.set_status(404) #resource not found
				self.response.write('No boats available to assign.')
			else:
				for b in all_boats:
					self.response.write(b)
					self.response.write('\n')
				self.response.set_status(404) #resource not found
				self.response.write('Enter boat id in URL (example: /boat/{id} to assign)')
	
	def patch(self, id): #modify boat
		try:
			boat_data = json.loads(self.request.body)
			boat = ndb.Key(urlsafe=id).get()
			boat.name = boat_data['name']
			boat.type = boat_data['type']
			boat.length = boat_data['length']
			boat.put()
			self.response.write(boat)
			self.response.write('\n')
			self.response.write('Boat updated successfully!')
		except:
			all_boats = Boat.query().fetch()
			if len(all_boats) < 1: #results returned for boats
				self.response.set_status(404) #resource not found
				self.response.write('No boats available to modify.')
			else:
				for b in all_boats:
					self.response.write(b)
					self.response.write('\n')
				self.response.set_status(404) #resource not found
				self.response.write('Enter boat id in URL (example: /boat/{id} to modify)')
			
class Slip(ndb.Model):
	id = ndb.StringProperty() #string generated by API
	number = ndb.IntegerProperty() #slip number
	current_boat = ndb.StringProperty() #id of the current boat, null if empty
	arrival_date = ndb.StringProperty() #string indicating the date boat arrived
	#departure_history = ndb.DateProperty(required=True, repeated=True)
	
class SlipHandler(webapp2.RequestHandler):
	def post(self): #create slip
		parent_key = ndb.Key(Slip, "Pier") #adding new slip to "Pier"
		slip_data = json.loads(self.request.body) #new slip data being entered
		new_slip = Slip(number=slip_data['number'], current_boat=slip_data['current_boat'], arrival_date=slip_data['arrival_date'], parent=parent_key) #receiving data from body
		new_slip.put()
		new_slip.id = new_slip.key.urlsafe()
		new_slip.put()
		slip_dict = new_slip.to_dict()
		slip_dict['self'] = '/slip/' + new_slip.key.urlsafe()
		self.response.write(json.dumps(slip_dict))
		
	def get(self, id=None): #view slip(s)
		if id: #return a single slip
			slip = ndb.Key(urlsafe=id).get()
			self.response.write(slip)
		else: #return all slips
			all_slips = Slip.query().fetch()
			for s in all_slips:
				if s.current_boat:
					slip_dict = s.to_dict()
					slip_dict['boat_url'] = '/boat/' + s.current_boat
					self.response.write('\n')
					self.response.write(json.dumps(slip_dict))
				else:
					slip_dict = s.to_dict()
					self.response.write('\n')
					self.response.write(json.dumps(slip_dict))

	def delete(self, id): #delete slip
		try: #get current boat in slip
			slip = ndb.Key(urlsafe=id).get()
			slip_boat_id = slip.current_boat
			self.response.write(slip)
			self.response.write('\n')
			if slip_boat_id: #update boat "at_sea" value to False
				boat = Boat.query(Boat.id == slip_boat_id).get()
				boat.at_sea = True
				boat.put()
				self.response.write(boat)
				self.response.write('\n')
			slip.key.delete()
			self.response.write('Slip deleted successfully!')
		except:
			all_slips = Slip.query().fetch()
			if len(all_slips) < 1: #results returned for slips
				self.response.set_status(404) #resource not found
				self.response.write('No slips available.')
			else:
				for s in all_slips:
					self.response.write(s)
					self.response.write('\n')
				self.response.set_status(404) #resource not found
				self.response.write('Enter slip id in URL (example: /slip/{id} to delete)')
		
	def put(self, id): #assign boat to slip
		try:
			slip = ndb.Key(urlsafe=id).get() #holds current slip
			slip_data = json.loads(self.request.body)
			boat = Boat.query(Boat.id == slip_data['current_boat']).get()
			if boat.at_sea == False: #checking if boat is already in slip
				self.response.write('Boat is currently in a slip.')
			else:
				slip = ndb.Key(urlsafe=id).get() #holds current slip
				slip.current_boat = slip_data['current_boat']
				slip.arrival_date = slip_data['arrival_date']
				slip.put()
				boat.at_sea = False
				boat.put()
				self.response.write(boat)
				self.response.write('\n')
				self.response.write(slip)
		except:
			all_boats = Boat.query().fetch()
			all_slips = Slip.query().fetch()
			if len(all_boats) < 1: #results returned for boats
				self.response.set_status(404) #resource not found
				self.response.write('No boats available to assign.')
			elif len(all_slips) < 1:
				self.response.set_status(404) #resource not found
				self.response.write('No slips available.')
			else:
				for b in all_boats:
					self.response.write(b)
					self.response.write('\n')
				self.response.set_status(404) #resource not found
				self.response.write('Enter boat id in request body (example: "current_boat": "{id}")')
			
	def patch(self, id): #modify slip
		try:
			slip_data = json.loads(self.request.body)
			slip = ndb.Key(urlsafe=id).get()
			slip.arrival_date = slip_data['arrival_date']
			slip.put()
			self.response.write(slip)
			self.response.write('\n')
			self.response.write('Slip updated successfully!')
		except:
			all_slips = Slip.query().fetch()
			if len(all_slips) < 1: #results returned for slips
				self.response.set_status(404) #resource not found
				self.response.write('No slips available to modify.')
			else:
				for s in all_slips:
					self.response.write(s)
					self.response.write('\n')
				self.response.set_status(404) #resource not found
				self.response.write('Enter slip id in URL (example: /slip/{id} to modify)')
		
#https://webapp2.readthedocs.io/en/latest/guide/handlers.html
class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.write('Boats & Slips')
		
allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods
app = webapp2.WSGIApplication([
	#adding pages
	('/', MainPage),
	('/boat', BoatHandler),
	('/boat/(.*)', BoatHandler),
	('/slip', SlipHandler),
	('/slip/(.*)', SlipHandler)
], debug=True)