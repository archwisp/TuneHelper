#!/usr/bin/python
import sys, os, csv
from tunehelper import logfile

if len(sys.argv) != 3:
    print "Usage: %s <logfile-directory> <threshold>" % (os.path.basename(sys.argv[0]))
    sys.exit(0)

directory = sys.argv[1]
threshold = sys.argv[2]

highest = 0

for filename in os.listdir(directory):
    if ".csv" in filename:
        for row in logfile.get_rows(directory + '/' + filename):
            ect = int(row['ect']) * 1.8 + 32

            if ect > int(threshold):
                print "%s: %s F" % (filename, str(ect))
                highest = ect
