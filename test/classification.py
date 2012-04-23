from __future__ import division
#tagger = NGramTagger('es')
from nltk import NaiveBayesClassifier
#from micorpus import get_review
from nltk.corpus.reader import TaggedCorpusReader
from nltk.corpus.util import LazyCorpusLoader
from nltk.corpus import stopwords
from nltk import trigrams


def get_features(trigr):
	#trigr = ( (w,t),(w,t),(w,t) )
	'''returns the features for a trigram'''
	return{
	'first_word:':(trigr[0][0]),
	'first_pos':(trigr[0][1]),
	'second_word':(trigr[1][0]),
	'second_pos':(trigr[1][1]),
	'third_word':(trigr[2][0]),
	'third_pos':(trigr[2][1]),
	}

def load_train_set():
	'''loads a training set for the classifier'''
	archivo = open('../data/classitest.txt','r')
	train_set  = []
	for linea in archivo:
		tup = eval(linea)
		train_set.append((get_features(tup[0]),tup[1]))

	return train_set

def read_sentences_corpus(reader = None):
	#reader = LazyCorpusLoader()
	#its overriding reader
	reader = TaggedCorpusReader('../data/', r'.*\.pos')
	'''
	create a corpus reader with the files in ../data/*.pos 
	this files contains sentences tagged, and are the bases of trainig, test sets. 
	'''

	pos_fileids = reader.fileids()[1]
	neg_fileids = reader.fileids()[0]

	pos_sents = reader.tagged_sents(pos_fileids)
	neg_sents = reader.tagged_sents(neg_fileids)

	#pos_sents = [[(word.lower(),tag) for word,tag in sent if word not in stopwords.words('english')] for sent in pos_sents ]
	#neg_sents = [[(word.lower(),tag) for word,tag in sent if word not in stopwords.words('english')] for sent in neg_sents ]

	return (pos_sents,neg_sents)

def chunks(sentences, n = 10):
	""" Yield successive n-sized chunks from sentences.
    """
	for i in xrange(0,len(sentences), n):
		yield sentences[i:i+n]

def get_trigrams(sentence):
	'''keeps a yield to trigrams for each sentence in the reader'''
	return trigrams(sentence)

class Metrics():
	
	def diversity(corpus):
		return len(corpus) / len (set(corpus))


def test_metrics(reader):
	#reader = LazyCorpusLoader()

	pos = reader.words(reader.fileids()[1])
	print 'tokens: {0}, vocabulary:{1}'.format(len(pos),len(set(pos)))
	print len(pos) / len(set(pos))

if __name__ == '__main_':
	reader = TaggedCorpusReader('../data/', r'.*\.pos')
	test_metrics(reader)

if __name__ == '__main__':
	reader = TaggedCorpusReader('../data/', r'.*\.pos')
	from nltk import word_tokenize, pos_tag
	train_set = load_train_set()
	classifier = NaiveBayesClassifier.train(train_set)

	#to classify we have to pass a trigram. 
	test = ['always helpfull staff','the room was small','big room and beds','the view is amazing','neighbourhood is a bit ugly','connected with metro']
	for t in test: 
		tagged_t = pos_tag(word_tokenize(t))
		print tagged_t
		for trig in trigrams(tagged_t):
			print trig
			print classifier.classify(get_features(trig))	
			print '------------'

	