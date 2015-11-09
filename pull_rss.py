import feedparser
import os
import rss_config
from datetime import datetime
from rss_config import RSS_LIST_DIR, rss_feeds
import sqlite3



class RSS():


	TIME_FORMAT  = '%Y-%m-%d_%H-%M-%S'
	db = sqlite3.connect('rss.db')


	def saveStoryToDB(feed_id, item):
		date = datetime.strptime(item['published'], '%a, %d %b %Y %H:%M:%S %Z')
		c = RSS.db.cursor()
		sDate = date.strftime(RSS.TIME_FORMAT)
		c.execute("INSERT INTO stories(feeds_id, date, title, content) VALUES (?,?,?,?)", (feed_id, sDate, item['title'], item['summary']))
		RSS.db.commit()

	def saveStoriesToDB(feed_id, items):
		stories = []
		for item in items:
			date = datetime.strptime(item['published'], '%a, %d %b %Y %H:%M:%S %Z')
			sDate = date.strftime(RSS.TIME_FORMAT)
			stories.append((
				feed_id,
				sDate,
				item['title'],
				item['summary']	
			))
		c = RSS.db.cursor()
		c.executemany("INSERT INTO stories(feeds_id, date, title, content) VALUES (?,?,?,?)", stories)
		RSS.db.commit()

	def pullStoriesToDB():
		c = RSS.db.cursor()
		feeds = c.execute('SELECT * FROM feeds')
		# id, outlet, topic, url, last_update
		feed_stories = {}
		feed = feeds.fetchone()
		updated = {}
		while(feed != None):
			feed_stories[feed[0]] = []
			last_updated = feed[4]
			if(last_updated != None):
				last_updated = datetime.strptime(last_updated, RSS.TIME_FORMAT)
			stories = feedparser.parse(feed[3])
			for i in range(0,len(stories)):
				date = datetime.strptime(stories['items'][i]['published'], '%a, %d %b %Y %H:%M:%S %Z')
				if last_updated == None or date > last_updated:
					feed_stories[feed[0]].append(stories['items'][i])
					if (feed[0] not in updated) or (date > datetime.strptime(updated[feed[0]][0], RSS.TIME_FORMAT)):
						updated[feed[0]] = (date.strftime(RSS.TIME_FORMAT), feed[0])
				else:
					break;
			feed = feeds.fetchone()

		for feed_id in feed_stories:
			RSS.saveStoriesToDB(feed_id, feed_stories[feed_id])
		c.executemany('UPDATE feeds SET last_updated=? where id=?', [updated[row] for row in updated])
		RSS.db.commit()

