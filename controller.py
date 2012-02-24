# -*- coding: utf-8 -*-
from model import ReviewsList
from model import Judge
from model import Grapher
from view import Drawer

if __name__ == '__main__':  
    l = ReviewsList()
    reviews = l.get_all_reviews()
    print 'analysing ' + str(len(reviews)) + ' reviews...'
    print 'setting ratings and other judicial matters...'
    j = Judge(reviews)
    print 'determining conflicts...'
    conflicts = j.get_conflicts()
    print 'creating graph...'
    g = Grapher(reviews, conflicts, j)
    print 'drawing graph...'
    Drawer.draw_graph(g.get_graph(), 'original_graph')
    
# EOF