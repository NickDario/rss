# 
# RSS variables
# 
RSS_LIST_DIR = '/var/rss_list'
RSS_TIME_FORMAT = '%a, %d, %b %Y %H:%M:%S %Z'

rss_feeds = {
	'top' : 'http://rss.cnn.com/rss/cnn_topstories.rss',
	'world': 'http://rss.cnn.com/rss/cnn_world.rss',
	'us' : 'http://rss.cnn.com/rss/cnn_us.rss',
	'pol' : 'http://rss.cnn.com/rss/cnn_allpolitics.rss',
	'tech' : 'http://rss.cnn.com/rss/cnn_tech.rss',
}

# 
# Sentiment Variables
# 
SENTIMATE_DIR = '/home/nick/repos/rss/dict'

raw_positive = open(SENTIMATE_DIR + '/positive-words.txt').readlines()
raw_negative = open(SENTIMATE_DIR + '/negative-words.txt').readlines()

positive_words = [word.rstrip('\n\r') for word in raw_positive]
negative_words = [word.rstrip('\n\r') for word in raw_negative]

