import feedparser
import os
import rss_config
from datetime import datetime
from rss_config import RSS_LIST_DIR, rss_feeds


FORMAT  = '%a, %d %b %Y %H:%M:%S %Z'

# 
# Returns datetime of last of a specific rss feed
# 
def getLatestDate(feedname):
	f = os.listdir(RSS_LIST_DIR)
	if(len(f) == 0): return None
	latest = None
	for name in f:
		aName = name.split('.')
		if(len(aName) != 2): continue
		if(aName[0] != feedname): continue
		date = datetime.strptime(aName[1], '%Y-%m-%d_%H-%M-%S')
		if(latest == None or date > latest):
			latest = date
	return latest

# 
# Writes an rss type/title/date item
# 
def writeStory(feedname, item):
	sDate = date.strftime('%Y-%m-%d_%H-%M-%S')
	filename = feedname + '.' + sDate	
	storyfile = open(RSS_LIST_DIR + '/' + filename, 'a+')
	storyfile.write(item['title'])
	storyfile.close()

# 
# Retrieves the rss feeds from the list of feeds and
# records any new ones
# 
def pullStories():
	for source in rss_feeds:
		last = getLatestDate(source)
		stories = feedparser.parse(rss_feeds[source])
		for i in range(0,len(stories)):
			date = datetime.strptime(stories['items'][i]['updated'], '%a, %d %b %Y %H:%M:%S %Z')
			if last == None or date > last:
				writeStory(source, stories['items'][i])
				i += 1
			else:
				break





