import feedparser
import os
import rss_config
from datetime import datetime
from rss_config import RSS_LIST_DIR, rss_feeds
import sqlite3



class RSS():

	TIME_FORMAT  = '%Y-%m-%d_%H-%M-%S'
	db = sqlite3.connect('rss.db')

	# 
	# Writes an rss type/title/date item
	# 
	def writeStoryToCSV(feedname, item):
		date = item['published']
		sDate = date.strftime('%Y-%m-%d_%H-%M-%S')
		filename = feedname + '.' + sDate	
		storyfile = open(RSS_LIST_DIR + '/' + filename, 'a+')
		storyfile.write(item['title'])
		storyfile.close()

	def saveStoryToDB(feed_id, item):
		date = datetime.strptime(item['published'], '%a, %d %b %Y %H:%M:%S %Z')
		c = RSS.db.cursor()
		sDate = date.strftime(RSS.TIME_FORMAT)
		c.execute("INSERT INTO stories(feeds_id, date, title, content) VALUES (?,?,?,?)", (feed_id, sDate, item['title'], item['summary']))
		RSS.db.commit()

	# 
	# Retrieves the rss feeds from the list of feeds and
	# records any new ones
	# 
	def pullStoriesToCSV():
		for source in rss_feeds:
			last = getLatestDate(source)
			stories = feedparser.parse(rss_feeds[source])
			for i in range(0,len(stories)):
				date = datetime.strptime(stories['items'][i]['published'], '%a, %d %b %Y %H:%M:%S %Z')
				if last == None or date > last:
					writeStory(source, stories['items'][i])
					i += 1
				else:
					break

	def pullStoriesToDB():
		c = RSS.db.cursor()
		feeds = c.execute('SELECT * FROM feeds')
		# id, outlet, topic, url, last_update
		feed = feeds.fetchone()
		updated = {}
		while(feed != None):
			last_updated = feed[4]
			if(last_updated != None):
				last_updated = datetime.strptime(last_updated, RSS.TIME_FORMAT)

			stories = feedparser.parse(feed[3])
			# Save first date as latest date
			for i in range(0,len(stories)):
				date = datetime.strptime(stories['items'][i]['published'], '%a, %d %b %Y %H:%M:%S %Z')
				if(i == 0):
					updated[feed[0]] = (date.strftime(RSS.TIME_FORMAT), feed[0])
				if last_updated == None or date > last_updated:
					RSS.saveStoryToDB(feed[0], stories['items'][i])
				else:
					break;
			feed = feeds.fetchone()

		c.executemany('UPDATE feeds SET last_updated=? where id=?', [updated[row] for row in updated])
		RSS.db.commit()


# 
# Returns datetime of last of a specific rss feed
# 
# def getLatestDate(feedname):
# 	f = os.listdir(RSS_LIST_DIR)
# 	if(len(f) == 0): return None
# 	latest = None
# 	for name in f:
# 		aName = name.split('.')
# 		if(len(aName) != 2): continue
# 		if(aName[0] != feedname): continue
# 		date = datetime.strptime(aName[1], '%Y-%m-%d_%H-%M-%S')
# 		if(latest == None or date > latest):
# 			latest = date
# 	return latest



