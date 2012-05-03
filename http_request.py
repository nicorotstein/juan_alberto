from controller import ListReviews
import cherrypy
import json

class Graph():
	@cherrypy.expose
	def arguments(self,pos="",neg=""):
		lr = ListReviews()
		data = lr.parseThis([pos],[neg])
		return data

class Stats():
	def __init__(self):
		pass

	@cherrypy.expose
	def freqfeature(self,pos="",neg=""):
		cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
		cherrypy.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
		lr = ListReviews()
		data = lr.parseTest([pos],[neg])
		json_data = json.dumps(data)
		return json_data

	@cherrypy.expose
	def totalposneg(self,pos="",neg=""):
		cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
		cherrypy.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
		lr = ListReviews()
		data = lr.parseTest([pos],[neg])

		tot_pos, tot_neg = 0, 0
		for feat in data['pos']:
			tot_pos += data['pos'][feat]

		for feat in data['neg']:
			tot_neg += data['neg'][feat]

		data = {'pos':tot_pos,'neg':tot_neg}
		json_data = json.dumps(data)
		return json_data

class Services(object):
	stats = Stats()
	graph = Graph()		
	
	@cherrypy.expose
	def index(self):
		return "call /stats for stats or /graph for the graph"

cherrypy.quickstart(Services())
	