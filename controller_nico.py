# -*- coding: utf-8 -*-
from model import ReviewsList
from model import Judge
from model import Grapher
from view import Drawer
from tools import Stopwatch

if __name__ == '__main__':
    s = Stopwatch()
    s.start()
    l = ReviewsList() # by now it generates a given number of random reviews
    reviews = l.get_all_reviews()
    print 'analysing ' + str(len(reviews)) + ' reviews...'

    s.split()

    # print 'creating graph...'
    g = Grapher(reviews)
    # print 'drawing graph...'
    Drawer.draw_gexfgraph(g.get_container(), 'original_graph')

    g.compress()
    # Drawer.draw_dotgraph(g.get_dotgraph(), 'final_graph')
    Drawer.draw_gexfgraph(g.get_container(), 'final_graph')


    # s.split()

    # print 'removing redundant reviews...'
    # g.remove_dupes()
    # # print 'drawing graph...'
    # # Drawer.draw_graph(g.get_graph(), 'non-redundant_graph')
    
    # s.split()

    # print 'resolving cycles...'
    # g.resolve_cycles()
    # print 'computing accepted reviews...'
    # g.set_warranted()
    # # print 'drawing graph...'
    # Drawer.draw_graph(g.get_graph(), 'no_annoying_cycles_graph')
    
    # s.split()

    # print 'compressing graph...'
    # g.compress()
    # print 'drawing graph...'
    # Drawer.draw_dotgraph(g.get_dotgraph(), 'compressed_graph')
    
    # s.split()

    # print 'removing redundant reviews in compressed graph'
    # g.remove_dupes()
    # print 'drawing graph...'
    # Drawer.draw_dotgraph(g.get_dotgraph(), 'compressed_non-redundant_graph')

    # s.split

    # print 'recompressing graph...'
    # g.compress()
    # print 'drawing graph...'
    # Drawer.draw_graph(g.get_graph(), 'recompressed_graph')

    # s.split()

    s.elapsed()
    
# EOF