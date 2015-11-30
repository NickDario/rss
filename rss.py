from __future__ import division
from rss_config import negative_words, positive_words
from pull_rss import RSS
from analyze import Analyze
from bag_analyze import BagAnalyze

import os
import sys
import sqlite3

RSS.pullStoriesToDB()

db = sqlite3.connect('rss.db')
c  = db.cursor()

bag = BagAnalyze()

stories = c.execute('SELECT id, title FROM stories WHERE sentiment IS NULL').fetchall()
for id, title in stories:
	sentiment = bag.analyzeSentence(title)
	c.execute('UPDATE stories SET sentiment=? WHERE id=?',(sentiment,id))
	db.commit()

