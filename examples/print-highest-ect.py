#!/usr/bin/python #vim: ts=4:sw=4:et
import sys, os, csv
from tunehelper import logfile 

if len(sys.argv) != 2:
    print "Usage: %s <logfile-directory>" % (os.path.basename(sys.argv[0]))
    sys.exit(0)

directory = sys.argv[1]

highest = {'ect': 0}

for filename in os.listdir(directory):
    for row in logfile.getRows(directory + '/' + filename):

        if row['ect'] > highest['ect']:
            highest = row

highest_f = highest['ect'] * 1.8 + 32
print("File: %s ECT: %s C (%s F)" % (filename, str(highest['ect']), str(highest_f)))

