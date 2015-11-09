from spacy.en import English, LOCAL_DATA_DIR
from rss_config import positive_words, negative_words
import os
STRING = __import__('string')

data_dir = os.environ.get('SPACY_DATA', LOCAL_DATA_DIR)
parse = English(data_dir=data_dir)



class Analyze():

	def __init__(self):
		data_dir = os.environ.get('SPACY_DATA', LOCAL_DATA_DIR)
		parse = English(data_dir=data_dir)

	def wordSentiment(word, neg=False):
		mod = -1 if neg else 1
		if word in positive_words:
			# print (mod, word, 'Pos')
			return 10 * mod
		if word in negative_words:
			# print (mod, word, 'Neg')
			return -10 * mod
		# print(mod, word, 'Neutral')		
		return 0

	def textSentiment(text):
		tokens = parse(text)
		neg = False
		sentiment = 0
		for t in tokens:
			if t.pos_ not in ['VERB', 'NOUN', 'ADJ', 'ADV']:
				continue
			if t.pos_ in ['ADV', 'ADJ'] and t.dep_ == 'neg':
				neg = True
				continue
			# print(t.lemma_, neg, Analyze.wordSentiment(t.lemma_, neg))
			sentiment += Analyze.wordSentiment(t.lemma_, neg)
			neg = False

		return sentiment

	def fileSentiment(textfile):
		try:
			f = open(textfile).read()
		except:
			return 0

		return Analyze.textSentiment(f)




# doc = nlp('Ask not for whom the bell tolls, it tolls for thee.')
# # print([(d, d.tag_, d.pos_) for d in doc])

# for t in doc:
#     print(t.orth_,t.ent_type_ if t.ent_type_ != "" else "(Not and entity)", t.dep_, t.head.orth_, [c.orth_ for c in t.lefts], [c.orth_ for c in t.rights])
#     # print(dependency_labels_to_root(t))


# doc2 = nlp('Beheading video follows U.S. raid')

# for t in doc2:
#     print(t.orth_,t.ent_type_ if t.ent_type_ != "" else "(Not and entity)", t.dep_, t.head.orth_, [c.orth_ for c in t.lefts], [c.orth_ for c in t.rights])
#     # print(dependency_labels_to_root(t))




