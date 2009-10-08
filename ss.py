#!/usr/bin/python
"""
TODO:
1. thread shit up
2. mutliple SQL connections per thread, some kind of pooling
"""

from nntplibx import NNTP_SSL
import re, time, os, sys, urllib2, rfc822, time, syslog
from pyPgSQL import PgSQL

def decode(s, encodings=('ascii', 'utf8', 'latin1')):
	for encoding in encodings:
		try:
			return s.decode(encoding)
		except UnicodeDecodeError:
			pass
	print "i failed to decode"
	#return s.decode('ascii', 'ignore')

def process_group(group,c,connection):
	
	docs_xml = ""
	
	last_article = 0

	not_in_db = False
	group_id = 0

	#guarantees group is in the DB
	"""
	read last good article for the group from DB or file
	"""
	#last_article = int(file('last_article','r').readlines()[0])
	c.execute("SELECT id, last_article FROM groups WHERE name = %s", (group,))
	rows=c.fetchall()
	if len(rows) > 0:
		last_article = int(rows[0][1])
		group_id = int(rows[0][0])
	else:
		print "ADDING %s to DB!" % (group)
		not_in_db = True
		c.execute("INSERT INTO groups (name, last_article) VALUES (%s, %s)", (group,0))
		connection.commit()
		c.execute("SELECT id FROM groups WHERE name = %s", (group,))
		group_id = int(c.fetchone()[0])

	print "last article is %s" % last_article
	
	#connect to usenet, with SSL! WOO!
	s=''
	try:
		s = NNTP_SSL('secure.news.astraweb.com', 443, 'nemik1', 'this1moois')
	except:
		return ("fail", 0)
	
	#group_table = group_to_table(group)
	#print group_table
	
	resp, count, first, last, name = s.group(group)
	
	print 'Group', name, 'has', count, 'articles, range', first, 'to', last
	
	tolerance = 10000
	#tolerance = 300
	
	#oldest = last
	if last_article == 0:# and not_in_db:
		latest = str(int(last) - tolerance)
		print "NOT IN DB! USING TOLERANCE OF %d!!!" % (tolerance)
	else:
		latest = str(last_article)
	to_do = int(last) - int(latest)
	print "\n------NOW PROCESSING %d ARTICLES FROM %s-----\n\n" % (to_do, group)
	syslog.syslog("NOW PROCESSING %d ARTICLES FROM %s" % (to_do, group))
	if to_do ==0:
		s.quit()
		return ("",0)

	s.quit()
	
	#split work of todo into 5,000 article chunks
	chunks = (to_do / 5000) + 1
	if chunks == 1:
		print "only 1 chunk"
		return process_chunk(latest, last, group, group_id, 1, chunks)

	end = int(latest)
	for chunk in range(1,chunks):
		if chunk == len(range(0,chunks)):
			print "last chunk"
			return process_chunk(end, last, group, group_id,chunk,chunks)
		process_chunk(end,end+5000, group, group_id,chunk,chunks)
		end = end+5000

def process_chunk(l0, l1, group, group_id,chunk,chunks):
	s=''
	try:
		s = NNTP_SSL('secure.news.astraweb.com', 443, 'nemik1', 'this1moois')
	except:
		return ("fail", 0)
	resp, count, first, last, name = s.group(group)
	
	print "\n------NOW PROCESSING CHUNK %d of %d (%d/%d) FROM %s-----\n\n" % (int(chunk),int(chunks),int(l0),int(l1),group)
	syslog.syslog("NOW PROCESSING CHUNK %d of %d (%d/%d) FROM %s" % (int(chunk),int(chunks),int(l0),int(l1),group))
	
	docs_xml = ""
	resp, subs = s.xover(str(l0), str(l1))
	
	#dictionary of files
	#key is file name which is subject_file
	#value is tuple of poster->String, date->Int(timestamp), subject_exact->String, total parts, list [] segments -> (), segment is tuple of (id, segment, size)
	files = {}
	id = 0
	for sub in subs: 
		size = sub[6]
		subject_exact = decode(sub[1])#.encode("utf-8").decode("utf-8")
		#maybe do this by looking for the pattern everywhere and taking the last one from the group, not just end of line? may files appearing as articles....
		subject_file = re.sub("\((\d+)\/(\d+)\)$", "", subject_exact)
		p = re.search("\((\d+)\/(\d+)\)$",subject_exact)
		#data PartInfo = Part (Int, Int)
		
		id = sub[0]
		
		poster = decode(sub[2])
		date_str = sub[3]
	
		#subject_file_id = query for it
		#if None subject_file_id insert into files

		#d = "Fri, 03 Jul 2009 19:31:58 +0200"
		date = int(time.mktime(rfc822.parsedate(date_str)))

		fid = 0
		
		#part is tuple w/ ints (part #, total)
		part=()
		try:
			part = (int(p.group(1)), int(p.group(2)))
		except:
			c.execute("SELECT id FROM articles WHERE id = %s", (sub[4],))
			aid = c.fetchone()
			if aid != None:
				continue
			else:
				try:
					print "ARTICLE: : %s" % subject_exact
				except:
					print "ARTICLE: fuck you print-ascii"
				#c.execute("INSERT INTO articles (id, group_id, subject, poster, date) VALUES (%s, %s, %s, %s, %s)", (sub[4], group_id, subject_exact, poster, date,))
				#c.execute("INSERT INTO articles (id, group_id, subject, poster, date, time) VALUES (%s, %s, %s, %s, %s, current_timestamp)", (sub[4], group_id, subject_exact, poster, date,))
				c.execute("INSERT INTO articles (id, group_id, subject, poster, date, time) VALUES (%s, %s, %s, %s, %s, (TIMESTAMP 'epoch' + %s * INTERVAL '1 second'))", (sub[4], group_id, subject_exact, poster, date,date,))
				connection.commit()
				continue
		
		#guaranteed the file will be in the DB
		c.execute("SELECT id FROM files WHERE subject = %s", (subject_file))
		subject_file_id = c.fetchone()
		if subject_file_id != None:
			subject_file_id = int(subject_file_id[0])
			fid = subject_file_id
		else:
			try:
				print "processing %s" % subject_file
			except:
				print "processing SOMETHING CAN'T BE PRINTED, fuck you ascii"
			#c.execute("INSERT INTO files (subject, name, poster, parts_total, date) VALUES (%s, %s, %s, %s, %s)", (subject_file, subject_file, poster, part[1], date))
			#c.execute("INSERT INTO files (subject, name, poster, parts_total, date, time) VALUES (%s, %s, %s, %s, %s, current_timestamp)", (subject_file, subject_file, poster, part[1], date))
			c.execute("INSERT INTO files (subject, name, poster, parts_total, date, time) VALUES (%s, %s, %s, %s, %s, (TIMESTAMP 'epoch' + %s * INTERVAL '1 second'))", (subject_file, subject_file, poster, part[1], date,date))
			connection.commit()

			headers = s.head(id)
			groups_posted = ""
			for header in headers[3]:
				if "Newsgroups: " in header:
					groups_posted = header.replace('Newsgroups: ','').split(',')
	
			if fid == 0:
				c.execute("SELECT id FROM files WHERE name = %s", (subject_file,))
				fid = int(c.fetchone()[0])
			#guarantee that group exists otherwise create it
			gid = 0
			for group in groups_posted:
				c.execute("SELECT id FROM groups WHERE name = %s", (group,))
				gid = c.fetchone()
				#if i dont have that group, add it
				if gid != None:
					gid = int(gid[0])
				else:
					c.execute("INSERT INTO groups (name, last_article) VALUES(%s, %s)", (group, 0,))
					connection.commit()
				if gid == 0:
					c.execute("SELECT id FROM groups WHERE name = %s", (group,))
					gid = int(c.fetchone())
				c.execute("SELECT id FROM file_group WHERE file_id = %s AND group_id = %s", (fid, gid,))
				exists = c.fetchone()
				if exists != None:
					continue
				else:
					c.execute("INSERT INTO file_group (file_id, group_id) VALUES (%s, %s)", (fid, gid,))
					connection.commit()

		#print "sub is %s, groups are %s" % (sub, groups_posted)
		#add part to parts table and associate with file
		try:
			c.execute("INSERT INTO parts (id, file_id, bytes, number) VALUES (%s, %s, %s, %s)", (sub[4], fid, size, part[0]))
			connection.commit()
		except:
			continue
	
	firprint = str("first article:"+subs[1][0]+"last article:"+subs[-1][0]+"id is "+id)
	print firprint
	syslog.syslog(firprint)
	c.execute("UPDATE groups SET last_article = %s WHERE name = %s", (subs[-1][0], group,))
	connection.commit()
	
	print "\n\n ---- STATUS OF %s UDPATED! ---- \n\n" % (group)
	syslog.syslog("STATUS OF %s UDPATED!" % (group))
	
	s.quit()
	return (docs_xml,subs[-1][0])

"""
initial DB connections
"""
connection = PgSQL.connect(None, "nntp", "nntp4lyfe", "localhost", "nntp", client_encoding="utf-8")
c = connection.cursor()

syslog.openlog('py-nntp-indexer',0,syslog.LOG_CRON)

docs_xml = ""

group_article = {}

for group in file('/media/server/nntp/watchlist','r').readlines():
	group = group.strip()
	if group[0] == '#':
		continue
	process_group(group, c,connection)

syslog.syslog("DONE!")

c.close()
connection.commit()
connection.close()
