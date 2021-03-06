standard_features = {'clean':'clean',
					'dirty':'clean',
					 'comfort':'comfort',
					 'location':'location',
					 'connection':'location',
					 'metro':'location',
					 'bus':'location',
					 'transport':'location',
					 'position':'location',
					 'services':'services',
					 'service':'services',
					 'internet':'services',
					 'facilities':'services',
					 'facility':'services',
					 'minibar':'services', 
					 'breakfast':'services',
					 'wifi':'services',
					 'wi-fi':'services',
					 'breakfast':'services',
					 'staff':'staff',
					 'employess':'staff',
					 'price':'price',
					 'prices':'price',
					 'cost':'cost',
					 'see':'view',
					 'view':'view', 
					 'sight':'view',
					 'look':'view',
					 'barman':'staff',
					 'lady':'staff',
					 'furniture':'ambience',
					 'ambience':'ambience',
					 'rooms':'comfort',
					 'bed':'comfort',
					 'noisy':'comfort',
					 'silent':'comfort',
					 'check':'staff'


					}

def filter_tags(lista,tags):
	return [(word,tag) for word,tag in lista if tag in tags]

def extract_features(lista):
	features =  [(standard_features[word.lower()],tag) for word,tag in lista if word.lower() in standard_features]
	feats_words = [word for word,tag in features]
	return list(set(feats_words))
	
if __name__ == '__main__':
	from classification import read_sentences_corpus
	pos,neg = read_sentences_corpus()
	for rev in pos[200:250]:
		print ' '.join([word for word,tag in rev])
		#only = filter_tags(rev,['NN'])
		features = extract_features(rev)
		print features

