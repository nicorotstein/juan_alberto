'''
Created on Nov 30, 2011

@author: nicorotstein

'''

# -*- coding: utf-8 -*-
NUM_RANDOM = 20

import tools
from tools import Serializer
from linguatools import NGramTagger
from linguatools import FeaturesGrammar
from linguatools import Parser
from nltk import word_tokenize
import random
# import networkx as nx1
import pygexf
from pygexf import Gexf
import nx

class Review():
    '''
    classdocs
    '''

    def __init__(self, revid = -1, positive = {'feats':[], 'text':[]}, negative = {'feats':[], 'text':[]}, gender = 'na', age_range = 'na'):
        '''
        Constructor
        '''
        # id is just a number for indi/visualisation purposes
        self.id = str(revid)
        # are we gonna attach a user to each review? what for?
        self.user = 'juani'
        self.gender = gender
        self.age_range = age_range
        self.undecided_feats = list(set(positive['feats']) & 
            set(negative['feats']))
        self.positive_text = positive['text']
        self.negative_text = negative['text']
        self.positive_feats = list(set(positive['feats']) - 
            set(self.undecided_feats))
        self.negative_feats = list(set(negative['feats']) - 
            set(self.undecided_feats))
        pluses = ['+' for i in range(len(self.positive_feats))]
        minuses = ['-' for i in range(len(self.negative_feats))]
        self.attributes = zip(pluses, self.positive_feats) + zip(minuses, 
            self.negative_feats)
        if self.undecided_feats != []:
            print "review " + self.id + " has inconsistent features: " +  str(list(self.undecided_feats))
            # print self.attributes
        self.rating = 0
        self.conflicting_fe = {}
        self.accrued = False # CHECK if this is deprecated

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
            for r in set(reviews) - set([self]):
                common_atts.append(set(self.attributes) & 
                    set(r.get_attributes()))
            rating = 0
            for a in common_atts:
                rating += len(list(a))
            self.rating = rating
            
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
        # same as above but biased .7 towards '+'
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
        return(self.id + ' | ' + self.get_formatted_atts() + '| (' + 
            str(self.rating) + ')')

    # def get_attributes(self):
    #     return [self.get_formatted_atts(), self.rating]

    def subset_label(self, included):
        return(self.id + ' | ' + str(list(included)) + ' | ' + 
            self.get_formatted_atts())

    def plain_label(self):
        return self.get_formatted_atts()
        
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
    '''
    :class::ReviewsList
    '''
    def __init__(self):
        '''constructor
        :attribute::self.list_reviews:the list of reviews
        '''
        self.list_reviews = []
        self.lang = 'en-us'
        self.load_data(2)
     
    def load_data(self,new=0):
        '''
        :method:: load_data  
        :param new: new == 0 try to load list already created, else create a new one.
        '''
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
        '''
        This method prints all the reviews by id and its positives and negatives tagged text. 
        '''
        for review in self.list_reviews:
            
            print '---REVIEW---'
            print 'rev id: ',review.id
            
            print 'pos: ', review.get_positive_text()
            print 'neg: ', review.get_negative_text()

    def get_review(self,n):
        '''
        :param n:the n-th element to retrieve
        :returns a review in the n-th position of list_reviews
        '''
        return self.list_reviews[n]

    def get_all_reviews(self):
        '''
        :returns all the list_reviews (list of reviews).
        '''
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
            
        return (rev1.rating == rev2.rating) ### !!! PUT THIS BACK and cac1 == cac2)  
        
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
    '''
    handles all things related to graph handling
    it keeps the graph and 
    a dictionary of nodes whose key is the node id 
    and the value is the node itself
    '''
    def __init__(self, nodes):
        self.cid = 0
        self.judge = Judge(nodes)
        edges = self.judge.get_conflicts()
        self.dotgraph = nx.DiGraph()
        self.graph_container = Gexf("Nico Rotstein", 
            "Arguiew (reviews as argumentation) graph")
        self.dotnodes = {}
        self.has_compressed = {}
        self.warranted = set([])
        self.redundant = {}
        for n in nodes:
            if n.attributes != []:
                self.dotgraph.add_node(n.id, shape="record", 
                    label=n.get_label())
                self.dotnodes[n.id] = n
        for (n1, n2) in edges:
            if self.judge.equivalent(n1, n2):
                self.dotgraph.add_edge(n1.id, n2.id, color="red", dir="both", 
                    label=n1.get_conf_label(n2))
                self.dotgraph.add_edge(n2.id, n1.id, color="transparent")
            else:
                (better, worse) = self.judge.get_better_review(n1, n2)
                self.dotgraph.add_edge(better.id, worse.id, 
                    label=better.get_conf_label(worse))
        self.prettyGraph()

    def get_container(self):
        graph = self.graph_container.addGraph("directed", 
            "static", "Arguiew graph")
        attWarrant = graph.addNodeAttribute("warranted", 
            "false", "boolean")
        attPosText = graph.addNodeAttribute("positive_text", "", 
            "string")
        attNegText = graph.addNodeAttribute("negative_text", "", 
            "string")
        attHasCompressed = graph.addNodeAttribute("has_compressed", "[]", 
            "liststring")
        attRedundant = graph.addNodeAttribute("redundant", "[]", "liststring")
        nodes = []
        for n in self.dotgraph.nodes():
            nodes.append(self.dotnodes[n])
        self.judge = Judge(nodes)
        edges = self.judge.get_conflicts()
        node_handlers = {}
        for n in nodes:
            i = graph.addNode(n.id, n.get_formatted_atts())
            node_handlers[n.id] = i
            i.addAttribute(attPosText, str(n.positive_text))
            i.addAttribute(attNegText, str(n.negative_text))
            if (self.has_compressed != {}):
                i.addAttribute(attHasCompressed, 
                    str(list(self.has_compressed[n.id])))
        for (n1,n2) in edges:
            graph.addEdge(n1.id + '-' + n2.id, n1.id, n2.id, 
                label=n1.get_conf_label(n2))
        for w in self.warranted:
            node_handlers[w].addAttribute(attWarrant, "true")
            node_handlers[w].setColor("20", "200", "20")
        for r in self.redundant.keys():
            node_handlers[r].addAttribute(attRedundant, str(self.redundant[r]))
        return self.graph_container

    def get_dotgraph(self):
        return self.dotgraph

    def get_warranted(self):
        return [self.dotnodes[w] for w in self.warranted]

    def resolve_cycles(self): 
        # capture all cycles
        cycles = nx.simple_cycles(self.dotgraph)
        # the kind of cycles we are interested in are either binary (eg, [1,2,1]) or
        # even-lengthed (eg, [0,1,2,0]) - here we capture the latter and flag them
        # as "blocked"- don't be fooled by the length of the list
        blocked = []
        for cycle in cycles:
            #if (len(cycle) % 2 == 0):
            blocked += cycle
        affected_by_cycles = []
        preds = {}
        succs = {}
        for cycle in cycles:
            # we store all predecessors of all cycles and compute all successors
            cycle_set = list(set(cycle))
            cycle_predecessors = tools.all_predecessors(self.dotgraph, cycle_set, [])
            cycle_predecessors = list(set(cycle_predecessors) - set(blocked))
            cycle_successors = tools.all_successors(self.dotgraph, cycle_set, [])
            preds[str(cycle)] = cycle_predecessors
            # whenever a cycle has no predecessors, it introduces undecidedness
            # hence we store all successors in a global list of nodes that are
            # "affected by cycles"
            if (cycle_predecessors == []):
                affected_by_cycles += cycle_successors
        # those cycles that have no predecessors or that their predecessors
        # are affected by cycles that have no predecessors or... and so on and so forth
        out = []
        for cycle in cycles:
            if (preds[str(cycle)] == []) or (set(preds[str(cycle)]) & 
                set(affected_by_cycles) == []):
                out += cycle
        if out != []:
            print "involved in improper cycles: ", out
            # print len(out), "reviews were involved in improper cycling"
        for o in set(out):
            self.dotgraph.remove_node(o)

    def prettyGraph(self):
        self.remove_dupes()
        # print 'resolving cycles...'
        # self.resolve_cycles()
        print 'computing accepted reviews...'
        self.set_warranted()

    def compress(self):
        print 'compressing graph...'
        self.compress()
        print 'removing redundant reviews in compressed graph'
        self.remove_dupes()

    def remove_dupes(self):
        removals = []
        remaining_nodes = set(self.dotgraph.nodes())
        self.redundant = {}
        while remaining_nodes != set([]):
            n = remaining_nodes.pop()
            for n2 in remaining_nodes:
                if set(self.dotnodes[n2].attributes).issubset(
                    set(self.dotnodes[n].attributes)):
                    removals.append((n2,n))
                    self.redundant[n] = []
        if removals != []:
            if len(set(removals)) == 1:
                print "1 review was redundant"
            else:
                print len(set(removals)), "reviews were redundant"
        print removals
        for (r, n) in set(removals):
            if r in self.dotgraph.nodes() and n in self.dotgraph.nodes():
                print "review " + r + " was redundant with " + n
                self.dotgraph.remove_node(r)
                if r in self.redundant.keys():
                    del self.redundant[r] # THIS ISN'T THE SOLUTION!!!
                self.redundant[n] += r

    def set_warranted(self):
        undefeated = set([node for (node,x) in self.dotgraph.edges()]) - \
                      set([node for (x,node) in self.dotgraph.edges()])
        undefeated |= set([node for node in self.dotgraph.nodes() 
                           # if nx.is_isolate(self.dotgraph, node)])
                            if self.dotgraph.is_isolate(node)])
        warranted = undefeated | self.judge.grounded(undefeated, 
            self.dotgraph, set([]), set([]))
        for w in warranted:
            self.dotgraph.add_node(w, style="filled", fillcolor="green")
        self.warranted = warranted
        print len(warranted), "reviews were accepted"

    def compress(self):
        first_stage = set([node for (node,x) in self.dotgraph.edges()]) - \
                      set([node for (x,node) in self.dotgraph.edges()])
        first_stage |= set([node for node in self.dotgraph.nodes() 
                           # if nx.is_isolate(self.dotgraph, node)])
                            if self.dotgraph.is_isolate(node)])
        defeat_stages = [first_stage] + self.stages(first_stage, first_stage)
        cs = []
        for stage in defeat_stages:
            cs += self.consistent_subsets(stage, self.warranted)
        compressed_dotnodes = {}
        has_compressed = {}
        compressed_warranted = set([])
        compressed_dotgraph = nx.DiGraph()
        for subset in cs:
            positive_feats = set([])
            negative_feats = set([])
            for i in subset:
                positive_feats |= set(self.dotnodes[i].get_positive_feats())
                negative_feats |= set(self.dotnodes[i].get_negative_feats())
                r = Review('c' + str(self.cid), 
                           {'feats': list(positive_feats),'text': ""}, 
                           {'feats': list(negative_feats),'text': ""})
            compressed_dotnodes[r.id] = r
            has_compressed[r.id] = subset
            self.cid += 1
            if subset.issubset(self.warranted):
                compressed_warranted.add(r.id)
                compressed_dotgraph.add_node(r.id, style="filled", 
                    fillcolor="green", shape="record", 
                    label=str(r.subset_label(subset)))
            else:
                compressed_dotgraph.add_node(r.id, shape="record", 
                    label=str(r.subset_label(subset)))
        for id1, n1 in has_compressed.items():
            for id2, n2 in has_compressed.items():
                for i in n1:
                    for j in n2:
                        ri = self.dotnodes[i]
                        rj = self.dotnodes[j]
                        if ri.in_conflict(rj) and \
                           not (id1, id2) in compressed_dotgraph.edges() and \
                           not (id2, id1) in compressed_dotgraph.edges():
                           compressed_dotgraph.add_edge(id1, id2, dir="none")
        self.warranted = compressed_warranted
        self.dotgraph = compressed_dotgraph
        self.dotnodes = compressed_dotnodes
        self.has_compressed = has_compressed
        self.redundant = {}

    def stages(self, fringe, so_far):
        next = set()
        for r in fringe:
            next = next | set(self.dotgraph.successors(r))
        next = next - so_far - fringe
        if next == set([]):
            return []
        else:
            return [next] + self.stages(next, so_far | fringe)

    def consistent_subsets(self, stage, warranted):
        elem = stage.pop()
        (incons, consis) = self.consistent_in_rest([elem], stage, warranted)
        if incons == set([]):
            return [consis]
        else:
            return [consis] + self.consistent_subsets(incons, warranted)

    def consistent_in_rest(self, elems, rest, warranted):
        if rest == set([]):
            return (set([]), set(elems))
        else:
            ss = set()
            ps = set()
            for elem in elems:
                ss |= set(self.dotgraph.successors(elem))
                ps |= set(self.dotgraph.predecessors(elem))
            next = rest.pop()
            if (next in ss or next in ps or set(elems).issubset(warranted) 
                and next not in warranted):
                (i, c) = self.consistent_in_rest(elems, rest, warranted)
                return (i | set([next]), c | set(elems))
            else:
                (i, c) = self.consistent_in_rest(elems + [next], rest, warranted)
                return (i, set(elems + [next]) | c)

class Stats():
    # def __init__(self):
    #     pass

    @classmethod
    def rate_features(cls, arguments):
        for arg in arguments:
            arg.set_rating(arguments)
        all_atts = [(op, fe, arg.rating) for arg in arguments \
            for (op, fe) in arg.attributes]
        # print 'all attributes', all_atts
        fe_set = set([fe for (op, fe, rating) in all_atts])
        ratings = {}
        for fe in fe_set:
            ratings['+', fe] = 0
            ratings['-', fe] = 0
        for (op, fe, rating) in all_atts:
            ratings[op, fe] += rating
        # print 'ratings', ratings
        fe_ratings = {}
        for fe in fe_set:
            fe_ratings[fe] = ratings['+', fe] - ratings['-', fe]
        # print fe_ratings
        print '\nFEATURES RATING'
        for (fe, rating) in fe_ratings.iteritems():
            if rating > 0:
                print fe, 'is accepted'
            elif rating == 0:
                print fe, 'is undecided'
            else:
                print fe, 'is rejected'
        return fe_ratings

    @classmethod
    def warranted_features(cls, warranted):
        warr_atts = set([att for arg in warranted for att in arg.attributes])
        warrants = {}
        print '\nWARRANTS'
        for (op, fe) in warr_atts:
            warrants[fe] = op
            if op == '+':
                print fe, 'is accepted'
            else:
                print fe, 'is rejected'
        return warrants

    @classmethod
    def count_features(cls, arguments):
        all_atts = [(op, fe) for arg in arguments \
            for (op, fe) in arg.attributes]
        # print 'all attributes', all_atts
        fe_set = set([fe for (op, fe) in all_atts])
        count = {}
        for fe in fe_set:
            count['+', fe] = 0
            count['-', fe] = 0
        for (op, fe) in all_atts:
            count[op, fe] += 1
        # print 'ratings', ratings
        fe_count = {}
        for fe in fe_set:
            fe_count[fe] = count['+', fe] - count['-', fe]
        # print fe_ratings
        print '\nFEATURES COUNT'
        for (fe, rating) in fe_count.iteritems():
            if rating > 0:
                print fe, 'is accepted'
            elif rating == 0:
                print fe, 'is undecided'
            else:
                print fe, 'is rejected'
        return fe_count


# if __name__ == '__main__':
    # g = Grapher()

# EOF