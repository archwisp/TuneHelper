#!/usr/bin/python
import sys, os, csv

if len(sys.argv) != 2:
    print "Usage: check-csv-files.py <logfile-directory>"
    sys.exit(0)

directory = sys.argv[1]

for filename in os.listdir(directory):
    
    if ".csv" in filename:
        rows = csv.reader(open(directory + '/' + filename, "r"), delimiter=",")
        
        for row in rows:
            if len(row) != 15:
                print filename
                continue
