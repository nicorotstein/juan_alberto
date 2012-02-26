'''
commonly used methods
'''

import time
import random
from pickle import load,dump

def remove_all_in_list(list_out, list_from):
	if list_out != []:
		try:
			list_from.remove(list_out[0])
		except ValueError:
			pass
		remove_all_in_list(list_out[1:], list_from)

def all_predecessors(graph, nodes, so_far):
	if nodes == []:
		return []
	else:
		next = []
		nodes = list(set(nodes))
		for node in nodes:
			next += graph.predecessors(node)
		next = list(set(next))
		remove_all_in_list(so_far, next)
		so_far += next
		all_predecessors(graph, next, so_far)
		return so_far

def all_successors(graph, nodes, so_far):
	if nodes == []:
		return []
	else:
		next = []
		nodes = list(set(nodes))
		for node in nodes:
			next += graph.successors(node)
		next = list(set(next))
		remove_all_in_list(so_far, next)
		so_far += next
		all_successors(graph, next, so_far)
		return so_far

def flip(two_things, p):
    return two_things[0] if random.random() < p else two_things[1]


'''
Created on Nov 24, 2011

@author: luchux
'''
class Serializer(object):
  
    @classmethod     
    def get_object(cls,file_name):
        try:
            fser = open(file_name,'r')            
            pick = load(fser)
            fser.close()
            print 'read object from file'
            return pick                    
    
        except IOError as (errno, strerror):
            print "I/O error({0}): {1}".format(errno, strerror)            
            raise
    
    @classmethod     
    def save_object(cls,obj,file_name):
        try:
            fser = open(file_name,'w')
            dump(obj,fser)
            fser.close()
            print 'saved object to file '
            return True
        
        except IOError as (errno, strerror):
            print "I/O error({0}): {1}".format(errno, strerror)            
            raise      
    
class Stopwatch(object):
	"""
	a stopwatch to keep track of time
	it has to be started and then
	you can check elapsed time from start
	or
	you can check "lap" by "lap"
	so that different portions of code
	can be compared in terms of absolute time
	"""
	def __init__(self):
		self.start_time = 0
		self.last_lap_time = 0
		self.last_split = 0

	def start(self):
		self.start_time = self.last_split = time.time()
		print "STOPWATCH - started"

	def elapsed(self):
		delta = time.time() - self.start_time
		if delta < 1:
			print "STOPWATCH - time elapsed: " + str(int(delta * 1000)) + " msec"
		else:
			print "STOPWATCH - time elapsed: %.2f" %delta + " sec"

	def begin_lap(self):
		self.last_lap_time = time.time()
		print "STOPWATCH - lap has begun"

	def end_lap(self):
		delta = time.time() - self.last_lap_time
		if delta < 1:
			print "STOPWATCH - lap time: " + str(int(delta * 1000)) + " msec"
		else:
			print "STOPWATCH - lap time: %.2f" %delta + " sec"

	def split(self):
		delta = time.time() - self.last_split
		if delta < 1:
			print "STOPWATCH - split time: " + str(int(delta * 1000)) + " msec"
		else:
			print "STOPWATCH - split time: %.2f" %delta + " sec"
		self.last_split = time.time()
		
	def ssplit(self, some_string):
		delta = time.time() - self.last_split
		if delta < 1:
			print "STOPWATCH - split time for " + some_string + ": " + str(int(delta * 1000)) + " msec"
		else:
			print "STOPWATCH - split time for " + some_string + ": %.2f" %delta + " sec"
		self.last_split = time.time()
# EOF