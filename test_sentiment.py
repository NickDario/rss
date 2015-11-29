from os import listdir
from nltk import word_tokenize, pos_tag
import string

def pSentimentBayes(word):
    pPos = p_totalwords / (p_totalwords + n_totalwords)
    pNeg = n_totalwords / (p_totalwords + n_totalwords)
    pWordPos = words[word]['positive'] / p_totalwords
    pWordNeg = words[word]['negative'] / n_totalwords
    return (pWordPos * pPos) / ((pWordNeg*pNeg) + (pWordPos*pPos))

def nSentimentBayes(word):
    pPos = p_totalwords / (p_totalwords + n_totalwords)
    pNeg = n_totalwords / (p_totalwords + n_totalwords)
    pWordNeg = words[word]['negative'] / n_totalwords
    pWordPos = words[word]['positive'] / p_totalwords
    return (pWordNeg * pNeg) / ((pWordNeg*pNeg) + (pWordPos*pPos))


POS_DIR_SENTENCES = './rt-polaritydata'
NEG_DIR_SENTENCES = './rt-polaritydata'
p_doc = open(POS_DIR_SENTENCES + '/rt-polarity.pos', encoding='latin-1')
n_doc = open(NEG_DIR_SENTENCES + '/rt-polarity.neg', encoding='latin-1')


p_lines = p_doc.readlines()
n_lines = n_doc.readlines()

p_training = p_lines[:1000]
n_training = n_lines[:1000]

p_testing  = p_lines[2000:3000]
n_testing  = n_lines[2000:3000]

words = {}
p_totalwords = 0
n_totalwords = 0

# Add positive words to word counts.
# Count total positive words
for line in p_testing:
    line_words = word_tokenize(line)
    for x,word in enumerate(line_words):
        w = str.lower(word)
        if w in string.punctuation or len(word) < 3:
            continue
        if w not in words:
            words[w] = {
                'positive':0,
                'negative':0,
                'posNext' : {},
                'posPrev' : {},
                'negNext' : {},
                'negPrev' : {}
            }
        words[w]['positive'] += 1

        try:
            prev1 = str.lower(line_words[x-1])
            if prev1 not in words[w]['posPrev']:
                words[w]['posPrev'][prev1] = 0
            words[w]['posPrev'][prev1] += 1
        except Exception as e:
            pass

        try:
            next1 = str.lower(line_words[x+1])
            if next1 not in words[w]['posNext']:
                words[w]['posNext'][next1] = 0
            words[w]['posNext'][next1] += 1
        except Exception as e:
            pass

    p_totalwords += len(line_words)

# Add negative words to word counts
# Count total negative words
for line in n_training:
    line_words = word_tokenize(line)
    for x, word in enumerate(line_words):
        w = str.lower(word)
        if w in string.punctuation or len(word) < 3:
            continue
        if w not in words:
            words[w] = {
                'positive':0,
                'negative':0,
                'posNext' : {},
                'posPrev' : {},
                'negNext' : {},
                'negPrev' : {}
            }
        words[w]['negative'] += 1

        try:
            prev1 = str.lower(line_words[x-1])
            if prev1 not in words[w]['negPrev']:
                words[w]['negPrev'][prev1] = 0
            words[w]['negPrev'][prev1] += 1
        except Exception as e:
            pass

        try:
            next1 = str.lower(line_words[x+1])
            if next1 not in words[w]['negNext']:
                words[w]['negNext'][next1] = 0
            words[w]['negNext'][next1] += 1
        except Exception as e:
            pass

    n_totalwords += len(line_words)

# Only using bayes with single words
p_sorted = sorted([(word, words[word]['positive']) for word in words], key=lambda x:-x[1])
n_sorted = sorted([(word, words[word]['negative']) for word in words], key=lambda x:-x[1])

bayes = {}
for word in p_sorted:
    if word[0] not in bayes:
        bayes[word[0]] = {
            'positive' : 0,
            'negative' : 0,
            'posNext' : words[word[0]]['posNext'],
            'posPrev' : words[word[0]]['posPrev'],
            'negNext' : words[word[0]]['negNext'],
            'negPrev' : words[word[0]]['negPrev']
        }
    bayes[word[0]]['positive'] = pSentimentBayes(word[0])

for word in n_sorted:
    if word[0] not in bayes:
        bayes[word[0]] = {
            'positive' : 0,
            'negative' : 0,
            'posNext' : words[word[0]]['posNext'],
            'posPrev' : words[word[0]]['posPrev'],
            'negNext' : words[word[0]]['negNext'],
            'negPrev' : words[word[0]]['negPrev']
        }
    bayes[word[0]]['negative'] = nSentimentBayes(word[0])

n_correct = 0
for line in n_testing:
    lw = word_tokenize(line)
    wc = 0
    n = 0
    for i, word in enumerate(lw):
        if word in bayes:
            if i > 0 and lw[i-1] in bayes[word]['posPrev']:
                continue
            if i < len(lw)-1 and lw[i+1] in bayes[word]['posNext']:
                continue
            n += bayes[word]['negative']
            wc += 1
    if(wc > 0):
        negProb = n/wc
        if(negProb > 0.5):
            n_correct += 1
print(str(n_correct) + '/' + str(len(p_testing)))

p_correct = 0 
for line in p_testing:
    lw = word_tokenize(line)
    wc = 0
    p = 0
    for i,word in enumerate(lw):
        if word in bayes:
            if i > 0 and lw[i-1] in bayes[word]['negPrev']:
                continue
            if i < len(lw)-1 and lw[i+1] in bayes[word]['negNext']:
                continue
            p += bayes[word]['positive']
            wc += 1
    if(wc > 0):
        posProb = p/wc
        if(posProb > 0.5):
            p_correct += 1

    # print(line, prob)
print(str(p_correct) + '/' + str(len(n_testing)))





