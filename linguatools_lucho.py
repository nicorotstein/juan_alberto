class PolarityClasifier():
    '''aca voy a implementar un tagger
    para reviews que no se sepan si son pos o neg, 
    utilizando como training la info del sitema, es decir
    los reviews pos y negs que ya vienen tageados.'''

    def train():
        pass
    
    def get_polarity(sentence):
        pass
    
class CorpusGenerator():
    def __init__(self):
        pass
    
    def convert_tag(self,tuple_tag):
        return "/".join(tuple_tag)

    def parse_data(self,list_reviews):          
        import codecs
        fw_pos = codecs.open("../data/rev_pos.pos",'w','utf-8')
        fw_neg = codecs.open("../data/rev_neg.pos",'w','utf-8')
        for review in list_reviews:
            print '---REVIEW---'
            print 'rev id: ',review.id
            
            print 'pos: ',review.review_text["text"][1]     
            pos_new = [self.convert_tag(tuple_tag) for tuple_tag in review.review_text["text"][1] ]
            fw_pos.write(u' '.join(pos_new))
            fw_pos.write(u'\n')
            fw_pos.write(u'\n')

            print 'neg: ', review.review_text["text"][3]
            neg_new=[self.convert_tag(tuple_tag) for tuple_tag in review.review_text["text"][3] ]
            fw_neg.write(u' '.join(neg_new))
            fw_neg.write(u'\n')
            fw_neg.write(u'\n')
            
        
        fw_pos.close()
        fw_neg.close()
    
    def word(self):
        for sent in self.reader.tagged_sents(['review_hotels_pos.pos']):
            print sent

class CorpusAnalysis():
    def __init__(self):
        self.punctuation = ['.',',',';','!','?','_','"','&',"'"]
        self.load()
        
    def load(self):
        from nltk.corpus.reader import TaggedCorpusReader
        from nltk.tokenize import WordPunctTokenizer
        self.reader = TaggedCorpusReader('../data/', r'.*\.pos')

    def words(self):
        print self.reader.words(['rev_pos.pos'])

    def ngrams(self,words,n=0):
        
        from nltk.corpus import stopwords
        word_list2 = [w for w in words if not w in stopwords.words('english') and not w in punctutation]

        wprev,wprev1,wprev2 = None,None,None
        for i in range(len(word_list2)):
            w = word_list2[i] 
            yield (wprev,wprev1,wprev2,w)
            wprev = wprev1
            wprev1 = wprev2
            wprev2 = w

    def freq_dist_words(self):
        from nltk import ConditionalFreqDist
        from nltk.model import NgramModel
        categories = ['rev_neg.pos','rev_pos.pos']
        cfd = ConditionalFreqDist((category, word) for category in categories for word in c.ngrams(c.reader.words(category)))       
        genres = ['rev_neg.pos', 'rev_pos.pos']
        modals = ['location','room','size','staff','excellent','poor','good','bad']

        print 'neg :', cfd.__getitem__('rev_neg.pos')       
        print 'pos :', cfd.__getitem__('rev_pos.pos')
        #lm = NgramModel(4, self.reader.words(['rev_neg.pos']))

    def freq_dist_tags(self):
        from nltk import ConditionalFreqDist
        from nltk.model import NgramModel        
        cfd = ConditionalFreqDist((tag,word) for (word,tag)  in c.reader.tagged_words(self.cat_pos) if word.isalpha())
        
        return cfd

    def MI(self):
        pass