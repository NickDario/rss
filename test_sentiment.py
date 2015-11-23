





# 
# P(Word|Positive)  =   we know a word is positive: whats the probability of it being <word>
# P(Positive)       =   Probability a word is positive in a document?
# P(Word|Negative)  =   knowing a word is negative: whats the probability of it being <word>
#
#
# P(Positive|Word)  =   P(Word|Positive)*P(Positive) / P(Word|Positive)+P(Word|Negative)
#                   =   we know the word, whats the probability it's positive
#                   =   given a word: whats the probability it's positive
#
#

















# print(rtags['NN'])


# rtags = {};
# for n in negativeReviews:
#     f = open(n,'r')
#     s = f.read()
#     tags = pos_tag(word_tokenize(s))
#     for tag in tags:
#         pos_stub = tag[1][:2]
#         if pos_stub not in rtags:
#             rtags[pos_stub] = {}
#         if tag[0] not in rtags[pos_stub]:
#             rtags[pos_stub][tag[0]] = 0
#         rtags[pos_stub][tag[0]] += 1;
#     break;

# print(rtags['NN'], rtags['JJ'])

# print(sorted(rtags['NN'].items(), key=lambda x:x[1]))
# print(sorted(rtags['JJ'].items(), key=lambda x:x[1]))



# mix up teach reviews and test reviews
# parse out sentiment words:
#   use top 250 from pos and negative
#   parse out noise
#   50 most common pos patterns (patterns with high percentage of pos/neg words)
#       start with pos/neg words
# 
# use tensor flow and softmax with vector of words + input words





