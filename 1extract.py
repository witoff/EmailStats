#! /usr/bin/python

import os
import sys
import re
import json
import time
from datetime import datetime
from os.path import isdir, isfile, join


def getemails(path):
	allfiles = []
	objs = [join(path, d) for d in os.listdir(path) if d[0] != '.']
	dirs = [d for d in objs if isdir(d)]
	files = [f for f in objs if isfile(f) and f[-4:]=='emlx']
	allfiles.extend(files)
	for d in dirs: allfiles.extend(getemails(d))
	return allfiles


class Email(object):
	
	def __init__(self):
		self.mfrom = None
		self.subject = None
		self.to = None
		self.cc = None
		self.ti = None
		self.tt = None
		self.date = None
		self.path = None
		self.regex = re.compile('<.*?>')
		self.id = None
		self.reply_to = None

	def isDone(self):
		return self.mfrom and self.subject and self.to and self.cc and self.ti and self.tt and self.date and self.path and self.id and self.reply_to


	def parse_emails(self, email_str):
		return self.regex.findall(email_str)
		
		
	def __str__(self):
		obj = self.serialize()
		desc = [("%s: %s" % (k, obj[k])) for k in obj]
		return '\n'.join(desc)

	def serialize(self):
		return { 'to' : self.to, 
				'subject' : self.subject,
				'from' : self.mfrom,
				'cc': self.cc,
				'ti': self.ti,
				'tt': self.tt,
				'date' : self.date,
				'path' : self.path, 
				'id' : self.id,
				'reply_to' : self.reply_to}

def getAllEmails(path, limit=None):
	allfiles = getemails(path)
	if limit:
		allfiles = allfiles[0:limit]

	count = 0
	emails = []
	for path in allfiles:
		count += 1
		f = file(path, 'rb')

		lines = f.readlines()
		em = Email()
		em.path = path
		if count%100==0:
			print 'count: ', count
		for i in range(len(lines)):
			l = lines[i]

			def ingest(i, lines):
				s = lines[i][0:-1]
				if lines[i+1][0] in [' ', '\t']:
					s += ingest(i+1, lines)
				return s

			if l[0:5] == 'From:': 
				em.mfrom = em.parse_emails(ingest(i, lines))
			elif l[0:2] == 'To':
				em.to = em.parse_emails(ingest(i, lines))
			elif l[0:2] == 'CC':
				em.cc = em.parse_emails(ingest(i, lines))
			elif l[0:7] == 'Subject':
				em.subject = ingest(i, lines)
			elif l[0:12] == 'Thread-Index':
				em.ti = ingest(i, lines)
			elif l[0:12] == 'Thread-Topic':
				em.tt = ingest(i, lines)
			elif l[0:4] == 'Date':
				em.date = ingest(i, lines)[6:]
				if em.date[-1] == ')':
					em.date = em.date[:-11].strip()
					em.date = datetime.strptime(em.date, '%a, %d %b %Y %H:%M:%S')
				elif em.date[0].isdigit():
					em.date = em.date[:-6]
					em.date = datetime.strptime(em.date, '%d %b %Y %H:%M:%S')
				else:
					em.date = em.date[:-6].strip()
					em.date = datetime.strptime(em.date, '%a, %d %b %Y %H:%M:%S')
				em.date = int(time.mktime(em.date.timetuple()))
			elif l[0:10] == 'Message-ID':
				em.id = em.parse_emails(ingest(i, lines))[0][1:-1]
			elif l[0:11] == 'In-Reply-To':
				em.reply_to = em.parse_emails(ingest(i, lines))
				if em.reply_to:
					em.reply_to = em.reply_to[0][1:-1]
			if em.isDone() or l.strip() == '':
				break
		if em.date:
			emails.append(em.serialize())
	print 'total emails: ' , len(emails)

	emails = sorted(emails, key=lambda x: x['date'])
	return emails

def main():
	if len(sys.argv) > 1:
		paths = [ sys.argv[1] ]
	else:
		path = '/Users/%s/Library/Mail/V2/' % os.getlogin()
		paths = [(path + m) for m in os.listdir(path) if '@' in m]
		
	for p in paths:
		name = p.split('/')[-1].split('@')[0]
		print '\nProcessing name: ' + name
		emails = getAllEmails(p)
		filename = '%s.json' % name
		f = file(filename, 'w')
		f.write(json.dumps(emails))
		f.close()
		print 'Wrote file: ' + filename


if __name__ == '__main__':
	main()
