from nltk import word_tokenize
from os import listdir 
import string

class BagAnalyze:

    def __init__(self):
        p_doc = open('./rt-polaritydata/rt-polarity.pos', encoding='latin-1')
        n_doc = open('./rt-polaritydata/rt-polarity.neg', encoding='latin-1')

        p_lines = p_doc.readlines()
        n_lines = n_doc.readlines()

        self.p_totalwords = 0
        self.n_totalwords = 0
        self.words = {}

        # Aggregate positive words into bag
        for line in p_lines:
            line_words = word_tokenize(line)
            for x,word in enumerate(line_words):
                w = str.lower(word)
                if w in string.punctuation or len(word) < 3:
                    continue
                if w not in self.words:
                    self.words[w] = {
                        'positive':0,
                        'negative':0,
                        'posNext' : {},
                        'posPrev' : {},
                        'negNext' : {},
                        'negPrev' : {}
                    }
                self.words[w]['positive'] += 1

                try:
                    prev1 = str.lower(line_words[x-1])
                    if prev1 not in self.words[w]['posPrev']:
                        self.words[w]['posPrev'][prev1] = 0
                    self.words[w]['posPrev'][prev1] += 1
                except Exception as e:
                    pass

                try:
                    next1 = str.lower(line_words[x+1])
                    if next1 not in self.words[w]['posNext']:
                        self.words[w]['posNext'][next1] = 0
                    self.words[w]['posNext'][next1] += 1
                except Exception as e:
                    pass

            self.p_totalwords += len(line_words)


        # Add negative words to word counts
        # Count total negative words
        for line in n_lines:
            line_words = word_tokenize(line)
            for x, word in enumerate(line_words):
                w = str.lower(word)
                if w in string.punctuation or len(word) < 3:
                    continue
                if w not in self.words:
                    self.words[w] = {
                        'positive':0,
                        'negative':0,
                        'posNext' : {},
                        'posPrev' : {},
                        'negNext' : {},
                        'negPrev' : {}
                    }
                self.words[w]['negative'] += 1

                try:
                    prev1 = str.lower(line_words[x-1])
                    if prev1 not in self.words[w]['negPrev']:
                        self.words[w]['negPrev'][prev1] = 0
                    self.words[w]['negPrev'][prev1] += 1
                except Exception as e:
                    pass

                try:
                    next1 = str.lower(line_words[x+1])
                    if next1 not in self.words[w]['negNext']:
                        self.words[w]['negNext'][next1] = 0
                    self.words[w]['negNext'][next1] += 1
                except Exception as e:
                    pass

            self.n_totalwords += len(line_words)

        p_sorted = sorted([(word, self.words[word]['positive']) for word in self.words], key=lambda x:-x[1])
        n_sorted = sorted([(word, self.words[word]['negative']) for word in self.words], key=lambda x:-x[1])

        # Create dictionary with baysian probabilities for words.
        self.bayes = {}
        for word in p_sorted:
            if word[0] not in self.bayes:
                self.bayes[word[0]] = {
                    'positive' : 0,
                    'negative' : 0,
                    'posNext' : self.words[word[0]]['posNext'],
                    'posPrev' : self.words[word[0]]['posPrev'],
                    'negNext' : self.words[word[0]]['negNext'],
                    'negPrev' : self.words[word[0]]['negPrev']
                }
            self.bayes[word[0]]['positive'] = self.pSentimentBayes(word[0])

        for word in n_sorted:
            if word[0] not in self.bayes:
                self.bayes[word[0]] = {
                    'positive' : 0,
                    'negative' : 0,
                    'posNext' : self.words[word[0]]['posNext'],
                    'posPrev' : self.words[word[0]]['posPrev'],
                    'negNext' : self.words[word[0]]['negNext'],
                    'negPrev' : self.words[word[0]]['negPrev']
                }
            self.bayes[word[0]]['negative'] = self.nSentimentBayes(word[0])


    def pSentimentBayes(self,word):
        pPos = self.p_totalwords / (self.p_totalwords + self.n_totalwords)
        pNeg = self.n_totalwords / (self.p_totalwords + self.n_totalwords)
        pWordPos = self.words[word]['positive'] / self.p_totalwords
        pWordNeg = self.words[word]['negative'] / self.n_totalwords
        return (pWordPos * pPos) / ((pWordNeg*pNeg) + (pWordPos*pPos))


    def nSentimentBayes(self,word):
        pPos = self.p_totalwords / (self.p_totalwords + self.n_totalwords)
        pNeg = self.n_totalwords / (self.p_totalwords + self.n_totalwords)
        pWordNeg = self.words[word]['negative'] / self.n_totalwords
        pWordPos = self.words[word]['positive'] / self.p_totalwords
        return (pWordNeg * pNeg) / ((pWordNeg*pNeg) + (pWordPos*pPos))

    def analyzeSentence(self,sentence):
        wordlist = word_tokenize(sentence)
        wc = 0 # word count

        n = 0  # percent negative
        for i, word in enumerate(wordlist):
            if word in self.bayes:
                if i > 0 and wordlist[i-1] in self.bayes[word]['posPrev']:
                    continue
                if i < len(wordlist)-1 and wordlist[i+1] in self.bayes[word]['posNext']:
                    continue
                n += self.bayes[word]['negative']
                wc += 1

        p = 0  # percent positive
        for i, word in enumerate(wordlist):
            if word in self.bayes:
                if i > 0 and wordlist[i-1] in self.bayes[word]['negPrev']:
                    continue
                if i < len(wordlist)-1 and wordlist[i+1] in self.bayes[word]['negNext']:
                    continue
                p += self.bayes[word]['positive']
                wc += 1

        return {'positive':p/wc, 'negative':n/wc}

