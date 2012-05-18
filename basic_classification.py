standard_features = {'clean':'clean',
					 'dirty':'clean',
					 'comfort':'comfort',
					 'comfy':'comfort',
					 'location':'location',
					 'located':'location',
					 'situated':'location',
					 'connection':'location',
					 'club':'fun',
					 'clubs':'fun',
					 'nightlife':'fun',
					 'night life':'fun',
					 'bar':'fun',
					 'bars':'fun',
					 'metro':'location',
					 'bus':'location',
					 'area':'location',
					 'transport':'location',
					 'position':'location',
					 'services':'services',
					 'service':'services',
					 'parking':'services',
					 'internet':'services',
					 'facilities':'building',
					 'facility':'building',
					 'outside':'building',
					 'facade':'building',
					 'exterior':'building',
					 'minibar':'services', 
					 'wifi':'services',
					 'wi-fi':'services',
					 'breakfast':'restaurant',
					 'restaurant':'restaurant',
					 'food':'restaurant', 
					 'staff':'staff',
					 'employess':'staff',
					 'reception':'staff', 
					 'personnel': 'staff',
					 'price':'price',
					 'prices':'price',
					 'value':'price',
					 'money':'price',
					 'cost':'cost',
					 'see':'view',
					 'view':'view', 
					 'sight':'view',
					 'barman':'staff',
					 'lady':'staff',
					 'furniture':'ambience',
					 'ambience':'ambience',
					 'rooms':'comfort',
					 'room':'comfort',
					 'bed':'comfort',
					 'shower':'comfort',
					 'noisy':'quiet',
					 'silent':'quiet',
					 'quiet':'quiet',
					 'loud':'quiet',
					 'calm':'quiet',
					 'spa':'extras',
					 'jacuzzi':'extras',
					 'pool':'extras',
					 'smell':'comfort',
					 'smelly':'comfort',
					 'check':'staff',
					 'nothing':'nothing'
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

