#!/usr/bin/python
"""
nntp-scraper.py

SOLR:
	OK! 1. find way to keep track of last articles. could actually use DB for this but also text files, whatever. Use SQLite then though.
	OK! 2. for each file, construct a <doc> to be inserted and append to a giant update XML to be updated, but AT THE END! Update all groups checked at once,
	OK! 3. maybe commit doc add for each group instead of all at once at the end...
	OK! 4. get all headers of file only when necessary!  

TODO:
OK! 1. connect to some sqlite or something to keep track of which article id's for groups were last scraped (so only do new posted content)
1. thread shit up
2. check if solr is up first before processing anything. if not, exit and don't bother with usenet connection
3. find way to group files BY SUBJECT into artist/album nzb, so generate 1 for each complete album
	i. find way to parse the [11/14] other shit of albums in the middle of subject to collect total parts and see if all parts of album are there or not
		OK! YAY SOLR! a. tokenize subject into words separated by spaces, find similarities based on same positions of same tokens
		this can be a solr job
"""

from nntplibx import NNTP_SSL
import re, time, os, sys, urllib2
from xml.sax.saxutils import escape
from xml.sax.saxutils import quoteattr
import sqlite3

#import MySQLdb

def add_to_solr(add_xml):
	print "\n\n ---- ADDING FILES TO SOLR! ----\n"
	url = 'http://localhost:8983/solr/update'
	req = urllib2.Request(url, add_xml)
	req.add_header('Content-type','text/xml; charset=utf-8')
	response = urllib2.urlopen(req)
	the_page = response.read()
	print the_page

def commit_solr():
	print "\n\n ---- COMMITING SOLR! ----\n"
	url = 'http://localhost:8983/solr/update'
	req = urllib2.Request(url, "<commit/>")
	req.add_header('Content-type','text/xml; charset=utf-8')
	response = urllib2.urlopen(req)
	the_page = response.read()
	print the_page

def optimize_solr():
	print "\n\n ---- OPTIMIZING SOLR! ----\n"
	url = 'http://localhost:8983/solr/update'
	req = urllib2.Request(url, "<optimize/>")
	req.add_header('Content-type','text/xml; charset=utf-8')
	response = urllib2.urlopen(req)
	the_page = response.read()
	print the_page

def process_group(group,c,connection):
	
	docs_xml = ""

	"""
	xml escaper
	"""
	def xml_escape(string):
		return escape(quoteattr(string))
	
	def group_to_table(string):
		return string.replace('.','_').replace('-','__')
	
	def table_to_group(string):
		return string.replace('__','-').replace('_','.')
	
	
	#define group here, pull from DB? pass as arg?
	#group = sys.argv[1]
	#group = 'alt.binaries.sounds.mp3.gothic-industrial'
	#group = 'alt.binaries.e-book.technical'
	
	last_article = 0

	not_in_db = False
	"""
	check if group exists in DB
	"""
	c.execute('SELECT id FROM groups where name = ?', (group,))
	rows=c.fetchall()
	if len(rows)<1:
		print "ADDING %s to DB!" % (group)
		not_in_db = True
		c.execute('INSERT INTO groups (name, last_article) VALUES (?, 0)', (group,))
		connection.commit()


	"""
	read last good article for the group from DB or file
	"""
	#last_article = int(file('last_article','r').readlines()[0])
	c.execute('SELECT last_article FROM groups WHERE name = ?', (group,))
	rows=c.fetchall()
	if len(rows) > 0:
		last_article = rows[0][0]
	print last_article
	
	#connect to usenet, with SSL! WOO!
	s=''
	try:
		s = NNTP_SSL('secure.news.astraweb.com', 443, 'username', 'hahaha')
	except:
		return ("fail", 0)
	
	#group_table = group_to_table(group)
	#print group_table
	
	resp, count, first, last, name = s.group(group)
	
	print 'Group', name, 'has', count, 'articles, range', first, 'to', last
	
	tolerance = 10000
	#tolerance = 100
	
	#oldest = last
	if last_article == 0 and not_in_db:
		latest = str(int(last) - tolerance)
		print "NOT IN DB! USING TOLERANCE OF %d!!!" % (tolerance)
	else:
		latest = str(last_article)
	to_do = int(last) - int(latest)
	print "\n------NOW PROCESSING %d ARTICLES FROM %s-----\n\n" % (to_do, group)
	
	if to_do ==0:
		s.quit()
		return ("",0)

	resp, subs = s.xover(latest, last)
	
	#dictionary of files
	#key is file name which is subject_file
	#value is tuple of poster->String, date->Int(timestamp), subject_exact->String, total parts, list [] segments -> (), segment is tuple of (id, segment, size)
	files = {}
	
	for sub in subs: 
		size = sub[6]
		subject_exact = sub[1]
		subject_file = re.sub("\((\d+)\/(\d+)\)$", "", subject_exact)
		p = re.search("\((\d+)\/(\d+)\)$",subject_exact)
		#data PartInfo = Part (Int, Int)
	
		#part is tuple w/ ints (part #, total)
		part=()
		try:
			part = (int(p.group(1)), int(p.group(2)))
		except:	
			continue
		id = sub[0]
		
		poster = sub[2]
		segment = re.sub("<|>","",sub[4])
		date_str = sub[3]
	
		segmentt = (segment, size, id, part[0])
	
		if subject_file in files:
			files[subject_file][0].append(segmentt)
		else:
			#                     0: 0        1     2   3          1      2       3         4              5      
			files[subject_file] = ([(segment, size, id, part[0])], group, poster, date_str, subject_exact, part[1])
	
	try:
		print "first article:",subs[1][0],"last article:",subs[-1][0]
	except:
		x=x
	
	#out = file('out.nzb','w')
	
	atotal = 0
	acompleted = 0
	
	last_good_article = [0]
	
	for k,v in files.items():
		subject_file = k
		segments = v[0]
		group  = v[1]
		poster = v[2]
		date = v[3]
		subject = v[4]
		total = v[5]
	
		collected = len(v[0])
	
		atotal += total
	
		if total == collected:
			acompleted += collected
			print k,"collected:",collected,"total:",total," DATE:",date
			segments_node = ""
			sample_id = segments[0][2]
			headers = s.head(sample_id)
			groups_posted = ""
			for header in headers[3]:
				if "Newsgroups: " in header:
					groups_posted = header.replace('Newsgroups: ','').split(',')

			for segment, size, id, part in segments:
				segments_node += '\n<segment bytes="%s" number="%d">%s</segment>' % (size, part, segment)
				last_good_article.append(int(id))

			group_node = ""
			for group in groups_posted:
				group_node += "\n<group>%s</group>\n" %(group)
			file_node = '\n<file poster=%s subject=%s>\n<groups>%s</groups>\n<segments>%s\n</segments>\n</file>' % (xml_escape(poster), xml_escape(subject), group_node, segments_node)
			
			#gather vars to create the doc
			utime = int(time.time())
			fields = "\n<field name=\"id\">%s</field>" % (xml_escape(subject_file))
			fields += "\n<field name=\"name\">%s</field>" % (xml_escape(subject_file))
			fields += "\n<field name=\"date\">%s</field>" % (xml_escape(date))
			fields += "\n<field name=\"utime\">%s</field>" % (utime)
			fields += "\n<field name=\"poster\">%s</field>" % (xml_escape(poster))
			fields += "\n<field name=\"nzb_xml\"><![CDATA[ %s ]]></field>" % (file_node)
			for group in groups_posted:
				fields += "\n<field name=\"newsgroup\">%s</field>" % (group)
			
			doc = "<doc>%s</doc>" % (fields)
			docs_xml += doc

	last_good_article = max(last_good_article)
	
	print "%d / %d\tLAST GOOD ARTICLE: %d" % (acompleted, atotal, last_good_article)
	
	s.quit()
	return (docs_xml,last_good_article)

"""
initial DB connections
"""
connection = sqlite3.connect('/media/1tb/nntp/nzb.db')
#connection = MySQLdb.connect (host='localhost', user='nzb', passwd='nzb', db='nzb') 
c = connection.cursor()

docs_xml = ""

group_article = {}

for group in file('/media/1tb/nntp/watchlist','r').readlines():
	group = group.strip()
	doc, la = process_group(group, c,connection)
	if doc == "fail":
		doc, la = process_group(group, c,connection)
	group_article[group]=la
	if doc:
		#docs_xml += doc
		add_xml = "<add>%s</add>" % (doc)
		add_to_solr(add_xml)
		commit_solr()
		if la != 0:
			c.execute('UPDATE groups SET last_article = ? WHERE name = ?', (la, group,))
		connection.commit()
		print "\n\n ---- STATUS OF %s UDPATED! LAST ARTICLE IS %d ---- \n\n" % (group, la)

print "\n\n ---- DONE! ----\n"

c.close()
connection.commit()
connection.close()
