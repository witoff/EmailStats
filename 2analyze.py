#! /usr/bin/python

import os
import sys
import re
import json
from datetime import datetime
from os.path import isdir, isfile, join
import time

def main():
	f = file('allemails.jpl.json', 'r')
	emails = json.loads(f.read())
	f.close()
	print 'analyzing %i emails' % len(emails)

	parseTime(emails)
	fDates = file('allemails2.jpl.json', 'w')
	fDates.write(json.dumps(emails))


	#for e in emails: print e
	doThreads(emails)
	doSender(emails)
	doOrgs(emails)


def parseTime(emails):
	for e in emails:
		if e.get('date'):
			try:
				if e['date'][-1] == ')':
					e['date'] = datetime.strptime(e['date'][6:-11].strip(), '%a, %d %b %Y %H:%M:%S')
				else:
					e['date'] = datetime.strptime(e['date'][6:-6].strip(), '%a, %d %b %Y %H:%M:%S')
				e['date'] = int(time.mktime(e['date'].timetuple()))
			except:
				print 'exception', sys.exc_info()[0]


def doThreads(emails):
	for e in emails:
		if 'subject' in e:
			e['ti'] = e['subject']
	print '\nTHREAD ANALYSIS'
	for ttype in ['ti', 'tt']:
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
					deltas.append((t_sorted[i+1]['date']-t_sorted[i]['date']).total_seconds())

		#print 'AVERAGE DELTA: ', float(sum(deltas))/len(deltas)
		
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
