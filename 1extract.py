#! /usr/bin/python

import os
import sys
import re
import json
import time
from datetime import datetime
from os.path import isdir, isfile, join

class Email(object):
	""" Hold and format an email"""

	reEmail = re.compile('<.*?>')
	
	def __init__(self):
		self.mfrom = None
		self.subject = None
		self.to = None
		self.cc = None
		self.ti = None
		self.tt = None
		self.date = None
		self.path = None
		self.id = None
		self.reply_to = None

	def is_done(self):
		obj = self.serialize()
		for k in obj:
			if not obj[k]: 
				return False
		return True

	def parse_emails(self, email_str):
		return Email.reEmail.findall(email_str)
		
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

	def __str__(self):
		obj = self.serialize()
		desc = [("%s: %s" % (k, obj[k])) for k in obj]
		return '\n'.join(desc)


def get_emails(path):
	""" recursively get all emails in and below this path """

	items = [join(path, d) for d in os.listdir(path) if d[0] != '.']
	dirs = [d for d in items if isdir(d)]
	files = [f for f in items if isfile(f) and f[-4:]=='emlx']

	for d in dirs: files.extend(get_emails(d))

	return files

def get_all_emails(path, limit=None):
	""" return an array of all serialized emails dicts inside this path, sorted by date """

	allfiles = get_emails(path)
	if limit:
		allfiles = allfiles[0:limit]

	emails = []
	for fn in allfiles:
		if len(emails)%100==0:
			print 'count: ', len(emails)

		em = Email()
		em.path = fn
		
		f = file(fn, 'rb')
		lines = f.readlines()
		for i in range(len(lines)):
			l = lines[i]

			def ingest(i, lines):
				s = lines[i][0:-1]
				if lines[i+1][0] in [' ', '\t']:
					s += ingest(i+1, lines)
				return s

			if l.startswith('From:'): 
				em.mfrom = em.parse_emails(ingest(i, lines))
			elif l.startswith('To'):
				em.to = em.parse_emails(ingest(i, lines))
			elif l.startswith('CC'):
				em.cc = em.parse_emails(ingest(i, lines))
			elif l.startswith('Subject'):
				em.subject = ingest(i, lines)
			elif l.startswith('Thread-Index'):
				em.ti = ingest(i, lines)
			elif l.startswith('Thread-Topic'):
				em.tt = ingest(i, lines)
			elif l.startswith('Date'):
				date = ingest(i, lines)[6:]
				components = date.split()
				if len(components)<4:
					print 'bad date components for: %s.  Skipping entry.' % date
					break	
				if ',' in components[0]:
					components = components[1:5]
				else:
					components = components[0:4]
				match = ['%d', '%b', '%Y', '%H:%M:%S']
				if len(components[2])==2:
					match[2] = '%y'
				if len(components[3].split(':'))==2:
					match[3] = '%H:%M'

				date = datetime.strptime(' '.join(components), ' '.join(match))
				em.date = int(time.mktime(date.timetuple()))

			elif l.startswith('Message-ID'):
				ids = em.parse_emails(ingest(i, lines))
				em.id = ids[0][1:-1] if ids else 'empty'
			elif l.startswith('In-Reply-To'):
				em.reply_to = em.parse_emails(ingest(i, lines))
				if em.reply_to:
					em.reply_to = em.reply_to[0][1:-1]
			if em.is_done() or l.strip() == '':
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
		path = '/Users/%s/Library/Mail/' % os.getlogin()
		def getBoxes(path):
			return [join(path,m) for m in os.listdir(path) if '@' in m]
		paths = getBoxes(path)

		for p in os.listdir(path):
			np = join(path,p)
			if os.path.isdir(np):
				paths.extend(getBoxes(np))
		
	for p in paths:
		name = p.split('/')[-1].split('@')[0]
		print '\nProcessing email account: ' + name
		emails = get_all_emails(p)
		filename = '%s.json' % name
		f = file(filename, 'w')
		f.write(json.dumps(emails))
		f.close()
		print 'Wrote file: ' + filename


if __name__ == '__main__':
	main()
