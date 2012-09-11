#! /usr/bin/python

import json
import sys
import pprint
import time
from datetime import datetime

assert len(sys.argv) > 1

data = json.loads(file(sys.argv[1], 'r').read())

f = open('emails.gource', 'w')

for d in data:
	f.write(str(d['date']))
	f.write('|')
	if d['from'] and len(d['from'])>0:
		f.write(d['from'][0])
	else:
		f.write('unknown')
	f.write('|A|')
	if 'subject' in d:
		f.write(str(d['subject']))
	elif 'tt' in d:
		f.write(str(d['tt']))
	else:
		f.write('unknown')
	f.write('|\n')
f.close()
print 'written to gource file'
