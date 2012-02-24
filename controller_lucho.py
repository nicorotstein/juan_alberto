from model import ReviewsList
from linguatools_lucho import CorpusAnalysis

if __name__ == '__main__':
	l = ReviewsList()
	print l.get_review(1).get_positive_feats()

	a = CorpusAnalysis()
	a.words()