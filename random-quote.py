#!/usr/bin/python
# Usage: python random-quote.py <highlights-file.json>
import os, sys
import json
import random

if len(sys.argv) < 2:
    print("Usage: python random-quote.py <highlights-file.json>")
    sys.exit(1)

if not os.path.exists(sys.argv[1]):
    print("Invalid input json file")
    sys.exit(1)
    
fp = open(sys.argv[1], 'r')
data = json.load(fp)

ind = random.randint(0,len(data)-1)
#print(ind)
#q = random.choice(data.values())
book = list(data.keys())[ind]
q = random.choice(data[book])
print("%s -- From: %s" %(q, book))