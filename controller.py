# -*- coding: utf-8 -*-
from model import ReviewsList
from model import Judge
from model import Grapher
from view import Drawer
from tools import Stopwatch
from nltk import word_tokenize
from linguatools import NGramTagger
from linguatools import Parser
from basic_classification import extract_features
from model import Review
#agregar server xmlrpc
#cada object review tine atributo rating

class ListReviews():
    def __init__(self):
        self.tagger = NGramTagger('en')

    def create_list_reviews(self,data_pos, data_neg):
        review_list = []
        count = 0
        print 'creating reviews...' 
                
        for revi_pos, revi_neg in zip(data_pos, data_neg):
            rev_id = count
            count += 1

            positive_tags = self.tagger.tag(word_tokenize(revi_pos))
            negative_tags = self.tagger.tag(word_tokenize(revi_neg))
            
            positive_feats = extract_features(positive_tags)
            negative_feats = extract_features(negative_tags)           

            positive = {'feats': positive_feats, 'text': positive_tags}
            negative = {'feats': negative_feats, 'text': negative_tags}

            review_list.append(Review(rev_id, positive, negative))

        return review_list


    def parseThis(self,pos,neg): 
        reviews = self.create_list_reviews(pos,neg)
        j = Judge(reviews)
        conflicts = j.get_conflicts()

        #por que pasas conflicts y j? 
        self.g = Grapher(reviews,conflicts,j)
        g = Grapher(reviews, conflicts, j)
        g.set_warranted()
        Drawer.draw_graph(g.get_graph(), 'compressed_graph')
        xml_file = open('data/compressed_graph.gexf','r')
        return xml_file.read()

def main():
    from SimpleXMLRPCServer import SimpleXMLRPCServer
    from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler

    # Restrict to a particular path.
    class RequestHandler(SimpleXMLRPCRequestHandler):rpc_paths = ('/RPC2',)

    # Create server
    server = SimpleXMLRPCServer(("localhost", 8000),
                            requestHandler=RequestHandler)
    server.register_instance(ListReviews())
    print "Listening on port 8000..."
    server.serve_forever()

if __name__ == '__main__':
    main()

