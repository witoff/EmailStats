#! /usr/bin/python

import json
import sys
import pprint
import time
from datetime import datetime

assert len(sys.argv) > 1

data = json.loads(file(sys.argv[1], 'r').read())

history = {}
def buildHistory():
	for d in data:
		history[d['id']] = d
	def dig(d):
		if 'treepath' not in d:
			if d['reply_to'] and d['reply_to'] in history:
				d['treepath'] = dig(history[d['reply_to']]) + '/' + d['subject']
			else:
				d['treepath'] = d['subject']
		return d['treepath']

	for d in data:
		dig(d)
	
buildHistory()

f = open(sys.argv[1].split('.')[0] + '.gource', 'w')

for d in data:
	f.write(str(d['date']))
	f.write('|')
	if d['from'] and len(d['from'])>0:
		f.write(d['from'][0])
	else:
		f.write('unknown')
	f.write('|A|')
	if 'treepath' in d:
		f.write(str(d['treepath']))
	elif 'subject' in d:
		f.write(str(d['subject']))
	elif 'tt' in d:
		f.write(str(d['tt']))
	else:
		f.write('unknown')
	f.write('|\n')
f.close()
print 'written to gource file: ' + f.name
