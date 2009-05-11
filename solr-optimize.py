#!/usr/bin/python
import re, time, os, sys, urllib2

def optimize_solr():
	print "\n\n ---- OPTIMIZING SOLR! ----\n"
	url = 'http://localhost:8983/solr/update'
	req = urllib2.Request(url, "<optimize/>")
	req.add_header('Content-type','text/xml; charset=utf-8')
	response = urllib2.urlopen(req)
	the_page = response.read()
	print the_page

optimize_solr()


print "\n\n ---- DONE! ----\n"

