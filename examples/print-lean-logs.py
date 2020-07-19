#!/usr/bin/python
import sys, os
from tunehelper import logfile

if len(sys.argv) != 2:
    print "Usage: %s <logfile-directory>" % (os.path.basename(sys.argv[0]))
    sys.exit(0)

directory = sys.argv[1]

for filename in os.listdir(directory):
    for row in logfile.get_rows(directory + '/' + filename):
            if row['throttle'] > 30 and row['load'] >= 80 and row['rpm'] > 4000 and row['ltr'] < 40 and row['afr'] > .89:
                print "File: %s  Sample: %s  Time: %s  Throttle: %s  Load: %s  Speed: %s  RPM: %s  AFR: %s  Cat: %s F" % (
                    filename, 
                    str(row['sample']).ljust(6), 
                    str(row['time']).ljust(10), 
                    str(row['throttle']).ljust(3), 
                    str(row['load_band']).ljust(3), 
                    str(row['speed']).ljust(3), 
                    str(row['rpm_band']).ljust(4), 
                    str(row['afr']).ljust(5), 
                    str(row['cat']).ljust(4)
                )
