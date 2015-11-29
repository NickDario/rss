from time import time
from nltk import word_tokenize, pos_tag

pos = open('/home/nick/repos/rss/rt-polaritydata/rt-polarity.pos', encoding='latin-1')

x = {}
lines = pos.readlines()
print('starting: ', str(time()))
print(lines[0])
for i, l in enumerate(lines):
	print(str(i)+ '/'+str(len(lines)), time())
	wl =word_tokenize(l)
	for w in wl:
		if w not in x:
			x[w] = 0
		x[w] += 1

words = []
for word in x:
	words.append(word)

tags = pos_tag(words)

print(tags)




