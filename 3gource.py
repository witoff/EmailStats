import json
import pprint
import time
from datetime import datetime

data = json.loads(file('allemails2.jpl.json', 'r').read())

f = open('emails.gource', 'w')

for d in data:
	f.write(str(d['date']))
	f.write('|')
	if d['from'] and len(d['from'])>0:
		f.write(d['from'][0])
	else:
		f.write('unknown')
	f.write('|A|')
	if 'tt' in d:
		f.write(str(d['tt']))
	else:
		f.write('unknown')
	f.write('|\n')
