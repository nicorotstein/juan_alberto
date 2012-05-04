# -*- coding: utf-8 -*-
from model import ReviewsList
from model import Judge
from model import Grapher
from view import Drawer
from nltk import word_tokenize
from nltk import pos_tag
from basic_classification import extract_features
from model import Review
from nltk.corpus.reader import TaggedCorpusReader
from collections import defaultdict
#agregar server xmlrpc
#cada object review tine atributo rating

class ReviewsContainer():
    def __init__(self):
        #self.tagger = NGramTagger('en')
        pass

    '''
    This method return pos_tagged reviews already stored in disk as corpus form. 
    '''
    def load_corpus_reviews(self,begin,end):
        #reader = LazyCorpusLoader()
        reader = TaggedCorpusReader('data/', r'.*\.pos')

        pos_fileids = reader.fileids()[1]
        neg_fileids = reader.fileids()[0]

        pos_sents = reader.tagged_sents(pos_fileids)
        neg_sents = reader.tagged_sents(neg_fileids)

        return (pos_sents[begin:end], neg_sents[begin:end])

    '''
    This method receive a list of reviews pos, neg in plain text, and pos_tagg them.  
    '''
    def tag_new_reviews(self,text_pos,text_neg):
        tags_pos = [pos_tag(word_tokenize(revi_pos)) for revi_pos in text_pos]
        tags_neg = [pos_tag(word_tokenize(revi_neg)) for revi_neg in text_neg]
        return tags_pos, tags_neg

    def create_list_reviews(self,tagged_pos, tagged_neg):
        review_list = []
        count = 0
        print 'creating reviews...' 
                
        for positive_tags, negative_tags in zip(tagged_pos, tagged_neg):
            rev_id = count
            count += 1
            positive_feats = extract_features(positive_tags)
            negative_feats = extract_features(negative_tags) 

            positive = {'feats': positive_feats, 'text': positive_tags}
            negative = {'feats': negative_feats, 'text': negative_tags}

            review_list.append(Review(rev_id, positive, negative))

        return review_list

    def get_statistics(self,pos,neg):
        loaded_pos, loaded_neg = self.load_corpus_reviews(200,250)
        user_pos, user_neg = self.tag_new_reviews(pos,neg)
        loaded_pos.extend(user_pos)
        loaded_neg.extend(user_neg)
        reviews = self.create_list_reviews(loaded_pos,loaded_neg)
        pos_stats = defaultdict(int)
        neg_stats = defaultdict(int)
        for review in reviews: 
            for feat in review.positive_feats:
                pos_stats[feat] += 1

            for feat in review.negative_feats:
                neg_stats[feat] += 1

        return{'pos':pos_stats, 'neg':neg_stats}

    def get_arguments_graph(self,pos,neg): 
        loaded_pos, loaded_neg = self.load_corpus_reviews(200,210)
        user_pos, user_neg = self.tag_new_reviews(pos,neg)
        loaded_pos.extend(user_pos)
        loaded_neg.extend(user_neg)
        reviews = self.create_list_reviews(loaded_pos,loaded_neg)

        self.g = Grapher(reviews)
        self.g.prettyGraph()
        Drawer.draw_dotgraph(self.g.get_dotgraph(), 'first_graph')
        Drawer.draw_gexfgraph(self.g.get_container(), 'first_graph')
        # every time get_container() is invoked, a new graph is generated
        self.g.recompress()
        Drawer.draw_dotgraph(self.g.get_dotgraph(), 'final_graph')
        Drawer.draw_gexfgraph(self.g.get_container(), 'final_graph')
        # final_graph.gexf contains both the original graph and the final one

        xml_file = open('data/final_graph.gexf','r')
        return xml_file.read()

    def test_rpc(self):
        return 'evtg ok'

def main():
    l = ReviewsContainer()
    print l.get_arguments_graph([],[])
    
if __name__ == '__main__':
    main()

