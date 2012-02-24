'''
commonly used methods
'''

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
    
# EOF