'''
Created on Nov 30, 2011

@author: nicorotstein

'''

NUM_RANDOM = 10

import tools
from tools import Serializer
# from linguatools import NGramTagger
# from linguatools import FeaturesGrammar
# from linguatools import Parser
# from nltk import word_tokenize
import random
import networkx as nx

class Review():
    '''
    classdocs
    '''

    def __init__(self, revid = -1, positive = {'feats':[], 'text':[]}, negative = {'feats':[], 'text':[]}, gender = 'na', age_range = 'na'):
        '''
        Constructor
        '''
        # id is just a number for visualisation purposes
        self.id = str(revid)
        # are we gonna attach a user to each review? what for?
        self.user = 'juani'
        self.gender = gender
        self.age_range = age_range
        self.positive_text = positive['text']
        self.negative_text = negative['text']
        self.positive_feats = positive['feats']
        self.negative_feats = negative['feats']
        pluses = ['+' for i in range(len(self.positive_feats))]
        minuses = ['-' for i in range(len(self.negative_feats))]
        self.attributes = zip(pluses, self.positive_feats) + zip(minuses, self.negative_feats)
        self.rating = 0
        self.conflicting_fe = {}
        self.accrued = False

    def get_positive_feats(self):
        return self.positive_feats

    def get_negative_feats(self):
        return self.negative_feats

    def get_positive_text(self):
        return self.positive_text

    def get_negative_text(self):
        return self.negative_text

    def get_attributes(self):
        return self.attributes
        
    def set_rating(self, reviews):
        if not self.accrued:
            common_atts = []
            for r in reviews:
                common_atts.append(set(self.attributes) & set(r.get_attributes()))
            rating = 0
            for a in common_atts:
                rating += len(list(a))
            #print self.id+':'+str(rating)
            self.rating = rating / 5
            
    def random_fillup(self, features, opinions):
        # number of attributes between 2 and 4 
        upper_bound = random.randrange(1,5)
        # features list shuffled in place
        random.shuffle(features)
        # list of random opinions with upper_bound length
        op_set = [random.choice(opinions) for i in range(upper_bound)]
        # an attribute is an opinion plus a feature in the first upper_bound positions in features list
        self.attributes = zip(op_set,features[0:upper_bound])

    def biased_random_fillup(self, features, opinions):
        opinionate = [tools.flip(opinions,.7) for i in range(len(features))]
        self.attributes = zip(opinionate,features[0:6])
        random.shuffle(self.attributes)
        upper_bound = random.randrange(1,5)
        self.attributes = self.attributes[0:upper_bound]
        
    def print_review(self):
        print self.id + '.',
        for (op,fe) in self.attributes:
            print op+fe,
        print ;
            
    def get_formatted_atts(self):
        atts = ""
        for (op,fe) in self.attributes:
            atts += op+fe
        return str(atts)
                    
    def get_label(self):
        return self.id + ' | ' + self.get_formatted_atts() + '| (' + str(self.rating) + ')'                
        
    def in_conflict(self, review):
        confs = [a1 for a1 in self.attributes for a2 in review.attributes if self.conflicting_attributes(a1,a2)]
        confatts = []
        for (op,fe) in confs:
            confatts.append((op,fe))
        self.conflicting_fe[review] = confatts
        return confs != []
    
    def get_conf_label(self, review):
        label = "/"
        for (op,fe) in self.conflicting_fe[review]:
            label += fe+'/'
        return str(label)
    
    def conflicting_attributes(self, (o1, f1), (o2, f2)):
        return o1 != o2 and f1 == f2

class ReviewsList():
    
    def __init__(self):
        
        self.list_reviews = []
        self.lang = 'en-us'
        self.load_data(2)
    
    def load_data(self,new=0):
        if(new == 0):
            try:
                self.list_reviews = Serializer.get_object('../data/reviews.dat')
            except:
                print 'impossible to load'
        elif new == 2:
            self.list_reviews = self.create_reviews([0 for n in range(NUM_RANDOM)], [1 for n in range(NUM_RANDOM)])
        else:
            self.parser = Parser(self.lang)
            self.grammar = FeaturesGrammar()
            self.tagger = NGramTagger(self.lang)
        
            url = "http://www.booking.com/reviewlist.en.html" 
            self.data_pos, self.data_neg = self.parser.get_from_url(url,50)
            self.list_reviews = self.create_reviews(self.data_pos, self.data_neg)
            self.save_reviews()

    def create_reviews(self, data_pos, data_neg):
        #todo: here will pass more parameters: name, age, etc
        review_list = []
        count = 0
        print 'creating reviews...' 
                
        for revi_pos, revi_neg in zip(data_pos, data_neg):
            rev_id = count
            count += 1

            positive_tags = []#self.tagger.tag(word_tokenize(revi_pos))
            negative_tags = []#self.tagger.tag(word_tokenize(revi_neg))

            #positive_atts = self.grammar.parse_features(tags_pos)
            #negative_atts = self.grammar.parse_features(tags_neg)
            
            l1 = ['bathroom','stuff','location','room','bed','breakfast','clean','food','price','friendly','atmosphere','size','tranquility']
            random.shuffle(l1)
            qpos = random.randrange(1, 3)
            qneg = random.randrange(0, 3)
            positive_feats = l1[0: qpos]
            negative_feats = l1[qpos + 1: qpos + qneg]

            positive = {'feats': positive_feats, 'text': positive_tags}
            negative = {'feats': negative_feats, 'text': negative_tags}

            review_list.append(Review(rev_id, positive, negative))

        return review_list
            
    def save_reviews(self):
        try:
            Serializer.save_object(self.list_reviews, '../data/reviews.dat') 
        except:
            print 'i/o error. Not saving'

    def list_features(self):
        for review in self.list_reviews:
            
            print '---REVIEW---'
            print 'rev id: ',review.id
            
            print 'pos: ', review.get_positive_feats()
            print 'neg: ', review.get_negative_feats()

    def list_pos_tags(self):
        for review in self.list_reviews:
            
            print '---REVIEW---'
            print 'rev id: ',review.id
            
            print 'pos: ', review.get_positive_text()
            print 'neg: ', review.get_negative_text()

    def get_review(self,n):
        return self.list_reviews[n]

    def get_all_reviews(self):
        return self.list_reviews

class Judge():
    '''
    use this class with a list of arguments, in order to determine 
    the existence of conflict and defeat between arguments
    use this class with a graph of arguments, in order to evaluate it
    and obtain the set of warranted arguments
    '''
    
    def __init__(self, arguments):
        # Arguments are a list of attributes, what a coincidence, just like reviews!
        self.arguments = arguments;
        self.attrib_count = {}
        self.attributes_set = set([att for arg in arguments for att in arg.attributes])
        for arg in arguments:
            arg.set_rating(arguments)
        self.count_features()
        
    def get_conflicts(self):

        return [(arg1, arg2) 
                for arg1 in self.arguments for arg2 in self.arguments
                if arg1.in_conflict(arg2) and arg1.id < arg2.id]
    
    def equivalent(self, rev1, rev2):
        # given that they are conflicting, rev1 and rev2 are equivalent
        # iff their rating is equal, and the count of conflicting attributes
        # is also equal
        # cac stands for conflicting_attributes_count
        cac1 = 0
        for conf_att in rev1.conflicting_fe[rev2]:
            cac1 += self.attrib_count[conf_att]
        cac2 = 0
        for conf_att in rev2.conflicting_fe[rev1]:
            cac2 += self.attrib_count[conf_att]
            
        return (rev1.rating == rev2.rating and cac1 == cac2)  
        
    def get_better_review(self, rev1, rev2):
        # given that they are conflicting, this method determines the best
        # review: the one with greater rating, or the one with greater count
        # of conflicting attributes if the reviews' rating is equal
        # retuns a tuple (best, worse)

        # !!! COULD BE DONE BETTER
        # THE "ATTRIBUTE SUPPORT" SHOULD BE STORED WHEN COMPUTING CONFLICTS 
        # print "checking for betterness: "+str(rev1.id)+" and "+str(rev2.id)
        cac1 = 0
        for conf_att in rev1.conflicting_fe[rev2]:
            cac1 += self.attrib_count[conf_att]
        cac2 = 0
        for conf_att in rev2.conflicting_fe[rev1]:
            cac2 += self.attrib_count[conf_att]

        if (rev1.rating > rev2.rating) or (rev1.rating == rev2.rating and cac1 > cac2):
            return (rev1, rev2)
        elif (rev1.rating < rev2.rating) or (rev1.rating == rev2.rating and cac1 < cac2):
            return (rev2, rev1)

    def count_features(self):
        for at in self.attributes_set:
            self.attrib_count[at] = 0
            for arg in self.arguments:
                if at in arg.attributes:
                    self.attrib_count[at] += 1

    def grounded(self, undefeated, graph, so_far, defeated_so_far):
        # recursive evaluation of the graph to obtain the set of
        # warranted arguments
        defeated = set()
        # get all the arguments defeated by those in "undefeated"
        # (which will be defeated)
        for u in undefeated:
            defeated = defeated | set(graph.successors(u))
        defeated = defeated - so_far - undefeated
        # take separately the new undefeated arguments, which are those
        # defeated by the defeated ones
        new_undefeated = set()
        for d in defeated:
            new_undefeated = new_undefeated | set(graph.successors(d))
        new_undefeated = new_undefeated - so_far - defeated - defeated_so_far
        inconsistent = set()
        for u in new_undefeated:
            if set(graph.predecessors(u)) & new_undefeated:
                inconsistent = inconsistent | set([u])
        new_undefeated = new_undefeated - inconsistent
        # if there are new undefeated arguments, iterate
        if new_undefeated != set([]):
            return new_undefeated | self.grounded(new_undefeated, 
                                                  graph, so_far | defeated | new_undefeated, 
                                                  defeated_so_far | defeated)
        else:
            return set([])

class Grapher():

    def __init__(self, nodes, edges, judge):
        self.graph = nx.DiGraph()
        self.blocked = []
        for n in nodes:
            self.graph.add_node(n.id, shape="record", label=n.get_label())
        for (n1, n2) in edges:
            if judge.equivalent(n1, n2):
                self.graph.add_edge(n1.id, n2.id, dir="both", label=n1.get_conf_label(n2))
                self.graph.add_edge(n2.id, n1.id, color="transparent")
                self.blocked.append((n1, n2))
            else:
                (better, worse) = judge.get_better_review(n1, n2)
                self.graph.add_edge(better.id, worse.id, label=better.get_conf_label(worse))

    def get_graph(self):
        return self.graph

if __name__ == '__main__':
    r = Review(999, {'text':[],'feats':[1,2,3]}, {'text':[],'feats':[4,5]})
    print r.attributes

# EOF