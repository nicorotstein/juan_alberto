from linguatools import NGramTagger
from linguatools import word_tokenize

#tagger = NGramTagger('es')

test =["Loved/NNP everything/VBG at/IN this/DT hotel/NN","Location/NN was/VBD ideal/JJ for/IN visiting/VBG tourist/NN attractions/NNS","Good/JJ size/NN hotel/NN room/NN","Great/WDT views/NNS from/IN room/NN","Friendly/RB and/CC helpful/JJ hotel/NN staff/NN"]
rev = []
for review in test:
	rev_list = review.split(" ")
	res = []
	for wordtag in rev_list:
		(word,tag) = wordtag.split("/")
		res.append((word,tag))
	rev.append(res)
print rev
a = [[('Loved', 'NNP'), ('everything', 'VBG'), ('at', 'IN'), ('this', 'DT'), ('hotel', 'NN')], [('$feature', 'NN'), ('was', 'VBD'), ('ideal', 'JJ'), ('for', 'IN'), ('visiting', 'VBG'), ('tourist', 'NN'), ('attractions', 'NNS')], [('Good', 'JJ'), ('$feature', 'NN'), ('hotel', 'NN'), ('room', 'NN')], [('Great', 'WDT'), ('$feature', 'NNS'), ('from', 'IN'), ('room', 'NN')], [('$feature', 'RB'), ('and', 'CC'), ('$feature', 'JJ'), ('hotel', 'NN'), ('staff', 'NN')]]

from nltk import trigrams
trigr = [trigrams(review) for review in a]
print trigr