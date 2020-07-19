#!/usr/bin/python #vim: ts=4:sw=4:et
import sys, os
from tunehelper import logfile, afrs

if len(sys.argv) != 2:
    print "Usage: %s <logfile-directory>" % (os.path.basename(sys.argv[0]))
    sys.exit(0)

directory = sys.argv[1]

for filename in os.listdir(directory):
    for row in logfile.getRows(directory + '/' + filename):
        if afrs.isRich(row):
            logfile.printRow(filename, row)
