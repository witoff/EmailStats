#! /usr/bin/python

import os
import sys
import re
import json
from datetime import datetime
from os.path import isdir, isfile, join
import time

def main():
	assert len(sys.argv)>1
	flags = ''
	if len(sys.argv)>2:
		flags = sys.argv[2]

	f = file(sys.argv[1], 'r')
	emails = json.loads(f.read())
	f.close()

	print 'Analyzing %i emails' % len(emails)

	doThreads(emails, flags)

	if 's' in flags:
		doSender(emails)
	if 'o' in flags:
		doOrgs(emails)


def doThreads(emails, flags):
	for e in emails:
		if 'subject' in e:
			e['ti'] = e['subject']
	print '\nTHREAD ANALYSIS'
	for ttype in ['ti', 'tt']:
		print '----'
		print 'TYPE: ', ttype
		threads = {}
		for e in emails: 
			if e[ttype]:
				if e[ttype] in threads:
					threads[e[ttype]].append(e)
				else:
					threads[e[ttype]] = [e]

		lens = [len(threads[t]) for t in threads]
		lens.sort()

		#Time Deltas
		deltas = []
		for t in threads:
			t_sorted = sorted(threads[t], key=lambda x: x['date'])
			for i in range(len(t_sorted)):
				if (i+1)<len(t_sorted):
					deltas.append(t_sorted[i+1]['date']-t_sorted[i]['date'])

		#print 'AVERAGE DELTA: ', float(sum(deltas))/len(deltas)
		
		duration = emails[-1]['date'] - emails[0]['date']
		dod = float(sum(deltas))/duration
		print 'Your DOD is: ' + str(dod)

		if 't' not in flags:
			break
		print 'Thread count: ', len(threads)
		print 'Longest thread: ', max(lens)
		print 'Shortest thread: ', min(lens)
		print 'avg: ', float(sum(lens))/len(lens)
		print 'sum: ', sum(deltas)


def doSender(emails):
	print '\nSENDER ANALYSIS'
	senders = {}
	for e in emails: 
		if not e.get('from') or len(e['from'])==0:
			continue
		by = e['from'][0]
		if by in senders:
			senders[by].append(e)
		else:
			senders[by] = [e]

	sentby_ordered = sorted(senders.items(), key=lambda x: len(x[1]))
	#print sentby_ordered
	for e in sentby_ordered:
		print len(e[1]), e[0]

def doOrgs(emails):
	fromto = {}
	regex = re.compile('.*@(.*)')
	for e in emails:
		if not e.get('from') or not e.get('to'):
			continue

		to = []
		for f in e['to']:
			matches = regex.match(f)
			if matches:
				to.extend(matches.groups())
		if e.get('cc'):
			for f in e['cc']:
				matches = regex.match(f)
				if matches:
					to.extend(matches.groups())
		to = set(to)

		for f in e['from']:
			matches = regex.match(f)
			if matches and len(matches.groups())>0:
				fromorg = matches.groups()[0]
				if fromorg not in fromto:
					fromto[fromorg] = {}
				for t in to:
					if t not in fromto[fromorg]:
						fromto[fromorg][t] = 0
					fromto[fromorg][t] += 1


	for fromorg in fromto:
		print '\n\n', fromorg, ' -> ' 
		for toorg in fromto[fromorg]:
			print '--%s :: %i' % (toorg, fromto[fromorg][toorg])

	print 'Num Orgs: ', len(fromto)

if __name__ == '__main__':
	main()
