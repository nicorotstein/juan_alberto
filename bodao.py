from nltk.corpus import TaggedCorpusReader
from basic_classification import extract_features
from model import Review
from nltk import pos_tag
from nltk import word_tokenize
#TODO: buenos comentarios
#Business Object --- 
#This object is responsible of creating the DAO (data access object), 
#who reads the data from storage. Here we create the model instances. 
class BusinessObject(object):
    def __init__(self):
        self.current_review_id = -1

    def create_review(self, text_pos, text_neg):
        postag_pos = pos_tag(word_tokenize(text_pos))
        postag_neg = pos_tag(word_tokenize(text_neg))

        feats_pos = extract_features(postag_pos)
        feats_neg = extract_features(postag_neg)

        self.current_review_id += 1

        positive_data = {'feats':feats_pos, 'text':postag_pos}
        negative_data = {'feats':feats_neg, 'text':postag_neg}

        return Review(revid=self.current_review_id, positive=positive_data, negative=negative_data )

    def read_review(self):
		dao = CorpusReader()
		objects = dao.get_objects()
		lista = []
		
		for postag_pos, postag_neg in zip(objects[0],objects[1]): 
			feats_pos = extract_features(postag_pos)
			feats_neg = extract_features(postag_neg)

			positive_data = {'feats':feats_pos, 'text':postag_pos}
			negative_data = {'feats':feats_neg, 'text':postag_neg}

    		lista.append(Review(revid = -1, positive = positive_data , negative = negative_data ))
    		#yield ({'pos':obj[0],'neg':obj[1]})
		return lista


#Data Access Objects - DAOs: These objects are responsible of defining an interface with the 
#differnet storages. 

class DBReader(object):
    def __init__(self):
        pass

    def get_objects(self,text_pos,text_neg):
        pass

class CorpusReader(object):
	def __init__(self):
		pass

	def get_objects(self):
		reader = TaggedCorpusReader('data/', r'.*\.pos')

		pos_fileids = reader.fileids()[1]
		neg_fileids = reader.fileids()[0]

		postag_pos = reader.tagged_sents(pos_fileids)
		postag_neg = reader.tagged_sents(neg_fileids)

		return (postag_pos, postag_neg)

    #reader = LazyCorpusLoader()

def main_bo():
	bo = BusinessObject()
	rev = bo.create_review("location and price","ambience and staff")
	print rev.positive_text
	print rev.positive_feats

def main_cr():
	cr = CorpusReader()
	print cr.get_objects()

if __name__ == '__main__':
	main_bo()