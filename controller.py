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
    g.resolve_cycles()
    Drawer.draw_graph(g.get_graph(), 'no_annoying_cycles_graph')
    g.remove_dupes()
    Drawer.draw_graph(g.get_graph(), 'no_dupes_graph')
    g.compress()
    Drawer.draw_graph(g.get_graph(), 'compressed_graph')
    
# EOF