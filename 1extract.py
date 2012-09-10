#! /usr/bin/python

import os
import re
import json
from os.path import isdir, isfile, join

#root = '/Users/%s/Library/Mail/V2/EWS-witoff@ums.jpl.nasa.gov' % os.getlogin()
root = '/Users/%s/Library/Mail/V2/IMAP-rob@api.gy@imap.gmail.com' % os.getlogin()

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
		self.to = None
		self.cc = None
		self.ti = None
		self.tt = None
		self.date = None
		self.path = None
		self.regex = re.compile('<.*?>')


	def parse_emails(self, email_str):
		return self.regex.findall(email_str)
		
		
	def __str__(self):
		return 'From: ' +  str(self.mfrom) + '\n' +\
		'To: ' + str(self.to) + '\n' +\
		'CC: ' + str(self.cc) + '\n' +\
		'ti: ' + str(self.ti) + '\n' +\
		'tt: ' + str(self.tt) + '\n' +\
		'date: ' +  str(self.date) + '\n' +\
		'path: ' + str(self.path)

	def serialize(self):
		return { 'to' : self.to, 
				'from' : self.mfrom,
				'cc': self.cc,
				'ti': self.ti,
				'tt': self.tt,
				'date' : self.date,
				'path' : self.path}




def getAllEmails(limit=None):
	allfiles = getemails(root)
	print 'total files: ' , len(allfiles)
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
				em.date = ingest(i, lines)
				break
		emails.append(em.serialize())
	return emails

def main():
	emails = getAllEmails()
	f = file('allemails.json', 'w')
	f.write(json.dumps(emails))
	f.close()


if __name__ == '__main__':
	main()
