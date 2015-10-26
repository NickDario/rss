
import nltk
from nltk.corpus import names
import string
import random

labeled_names = ([(name, 'male') for name in names.words('male.txt')] + [(name, 'female') for name in names.words('female.txt')])

random.shuffle(labeled_names)


def feature_set(word):
	features = {}
	features['first_letter'] = word[0].lower()
	features['suffix1']  = word[-1].lower()
	features['suffix2']  = word[-2].lower()
	for letter in string.ascii_lowercase:
		features['count({})'.format(letter)] = word.lower().count(letter)
		features['has({})'.format(letter)] = (letter in word.lower())
	return features


train_names = labeled_names[1500:]
devtest_names = labeled_names[500:1500]
test_names = labeled_names[:500]

train_set = [(feature_set(n), gender) for (n, gender) in train_names]
devtest_set = [(feature_set(n), gender) for (n, gender) in devtest_names]
test_set = [(feature_set(n), gender) for (n, gender) in test_names]

classifier = nltk.NaiveBayesClassifier.train(train_set)

errors = []
for (name, tag) in devtest_names:
	guess=classifier.classify(feature_set(name))
	if(guess != tag):
		errors.append((tag, guess, name))

for (tag, guess, name) in sorted(errors):
	print('correct={:<8} guess={:<8s} name={:<30}'.format(tag, guess, name))


print(nltk.classify.accuracy(classifier, test_set))



