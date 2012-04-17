'''
Created on Nov 30, 2011

@author: luchux
This module contains NLP tools based on NLTK class library. This tools are used for 
tokenization, tagging, chunks extraction, and features extraction.  

'''
from tools import Serializer
from nltk import word_tokenize
from nltk import RegexpParser
import requests
from bs4 import BeautifulSoup
import time

class NGramTagger(object):
    '''
    wrapper for nltk tagger
    A little tagger trained with unigrams, bigrams, trigrams
    and backoff training. 
    Todo: test and boostrap with review corpuss
    '''
    
    def __init__(self,language):
        
        '''
        :param:language
        :type lan string representing language to be used in the training 
        '''
        self.lang = language
        self.ser_path = "data/tagger.dat"
        self.init_tagger()
    
    def init_tagger(self):
        try:
            print 'loading tagger...'
            self.tagger = Serializer.get_object(self.ser_path) 
            print 'DONE...'           
            if self.tagger == False:
                print 'tagger not found in disk. Training one'
                self.tagger = self.train_classifier_tagger()
                print 'saving tagger to disk'
                Serializer.save_object(self.tagger, self.ser_path)
                print 'DONE...'
        except Exception:
            print Exception
            
    def tag(self,text):
        return self.tagger.tag(text)
   
    def backoff_tagger(self, train_sents, tagger_classes, backoff=None):
        for cls in tagger_classes:
            backoff = cls(train_sents, backoff=backoff)
        return backoff    
    
    def traintest_bigram_trigram_tagger(self):
        from nltk.tag import DefaultTagger,UnigramTagger, BigramTagger, TrigramTagger 
        from nltk.corpus import treebank        
        test_sents  = treebank.tagged_sents()[3000:]          
        train_sents = treebank.tagged_sents()[:3000]
        
        print 'trainging bigramTagger'                
        bitagger = BigramTagger(train_sents)
        print 'evaluation bitagger'
        print bitagger.evaluate(test_sents)
        
        print 'trainging trigram Tagger'
        tritagger = TrigramTagger(train_sents)
        print 'evaluation bitagger'
        print tritagger.evaluate(test_sents)
        print 'tagging'
     
           
    def traintest_uni_bi_tri_tagger(self):
        from nltk.tag import DefaultTagger,UnigramTagger, BigramTagger, TrigramTagger
        from nltk.corpus import conll2000, treebank    
        test_sents  = conll2000.tagged_sents()[8000:]          
        train_sents = treebank.tagged_sents()[3000:]
        print 'trainging trigramter with backoff'
        backoff = DefaultTagger('NN')
        tagger = self.backoff_tagger(train_sents, [UnigramTagger, BigramTagger,TrigramTagger], backoff=backoff)
        print 'evaluation trigram with backoff'        
        print tagger.evaluate(test_sents)
        print 'tagging'
        print tagger.tag(word_tokenize("This is a test. This should be faster than nothing. How can I rent a car in the next twelve hours? "))

    def train_classifier_tagger(self):
        from nltk.corpus import conll2000 
        from nltk.tag.sequential import ClassifierBasedPOSTagger    
        test_sents  = conll2000.tagged_sents()[9500:]          
        train_sents = conll2000.tagged_sents()
        print "training class"
        tagger = ClassifierBasedPOSTagger(train=train_sents)
        #print "evaluating"
        #print tagger.evaluate(test_sents)
        #print "tag"        
        return tagger

#chunker
class FeaturesGrammar():
    
 
    def __init__(self):
        self.grammar = r""" 
            FEATURE:
            {<JJ><NN|NNS>} 
              
            }<RB|RBR|RBS><JJ><NN|NNS>{
            {<RB|RBR|RBS><JJ><.*>}

            }<JJ><JJ><NN|NS>{
            {<JJ><JJ><.*>}

            }<NN|NNS><JJ><NN|NNS>{
            {<NN|NNS><JJ><.*>}
            {<NN|NNS><VB.*><JJ>} 
            {<RB|RBR|RBS><VB|VBD|VBN|VBG>$}
            
        """
    
    def parse_features(self,review):
        cp = RegexpParser(self.grammar)
        return cp.parse(review)

                
class Parser():
    '''
    This class crawls the web from one url, jumping in many offsets of pagination and extracting 
    all the reviews. 
    Todo: Now is crowling only one hotel. Crowling all the list of hotels, iterate over that list 
    applying get_reguest_url
    '''             
    def __init__(self,lang):
        self.lang = lang
    
    def parse(self, html):
        soup = BeautifulSoup(html)               
        #nombres  = soup.findAll(True,'cell_user_name');
        #ciudades = soup.findAll(True,'cell_user_location');
        #fechas   = soup.findAll(True,'dtreviewed');
        positives = soup.findAll(True, 'comments_good');
        negatives = soup.findAll(True, 'comments_bad');
        #puntuaciones = soup.findAll(True,'cell_score');
        positives = [comm.string.strip().replace('\n', ' ') for comm in positives]                     
        negatives = [comm.string.strip().replace('\n', ' ') for comm in negatives]
        
        return positives,negatives
    
    def get_request_url(self,url,max_page = 100):
        pos_tot,neg_tot = [],[]
        step = 25
        for i in range(0,1000,step):                          
            print  'pagina %d'%i
            results = requests.get(url, params = {
                'cc1':'fr',
                'sid':'17e1e96dcaaab2c671ad64fb6cf963d8',
                'pagename':'concorde-la-fayette',
                'offset':i,
                'rows':step,
                'sort':'language_relevance',
                'rid':'',
                'lang':self.lang
            })        
            pos,neg = self.parse(results.content)
            print 'parsed pos: ',len(pos)
            print 'parsed neg: ',len(neg)
            pos_tot.extend(pos)
            neg_tot.extend(neg)
             #&_=1329914466370"                        
        
        print 'neg_tot :',len(neg_tot)
        print 'pos_tot :',len(pos_tot)
        #Serializer.save_object(pos_tot,'../data/rev_pos.dat')
        #Serializer.save_object(neg_tot,'../data/rev_neg.dat')
        return pos_tot,neg_tot

    
if __name__ == '__main__':
    from model import ReviewsList

    l = ReviewsList()
    c = CorpusAnalysis()
    fd = c.freq_dist_tags()

    fd.tabulate()

    
    