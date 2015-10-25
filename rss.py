import feedparser
import os
from time import mktime
from datetime import datetime

feeds = {
	'top' : 'http://rss.cnn.com/rss/cnn_topstories.rss',
	'world': 'http://rss.cnn.com/rss/cnn_world.rss',
	'us' : 'http://rss.cnn.com/rss/cnn_us.rss',
	'pol' : 'http://rss.cnn.com/rss/cnn_allpolitics.rss',
	'tech' : 'http://rss.cnn.com/rss/cnn_tech.rss',
}

RSS_LIST_DIR = '/var/rss_list'


def getLastestDate(feedname):
	f = os.listdir(RSS_LIST_DIR)
	if(len(f) == 0): return False
	latest = None
	for name in f:
		aName = name.split('.')
		if(len(aName) != 2): continue
		if(aName[0] != feedname): continue
		date = datetime.strptime(aName[0], '%Y-%m-%d_%H-%M-%S')
		if(latest == None or date > latest):
			latest = date
	return latest

def writeStory(feedname, item):
	sDate = date.strftime('%Y-%m-%d_%H-%M-%S')
	filename = feedname + '.' + sDate	
	storyfile = open(RSS_LIST_DIR + '/' + filename, 'a+')
	storyfile.write(item['title'])
	storyfile.close()

for source in feeds:
	last = getLatestDate(source)
	stories = feedparser.parse(feeds[source])
	new = True
	i = 0
	while new:
		date = datetime.strptime(stories['items'][i]['updated'])
		if date > last:
			writeStore(source, stories['items'][i])
			i += 1
		else:
			new = False



