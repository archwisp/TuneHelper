#!/usr/bin/python
import sys, os
from tunehelper import logfile, rpm_bands, fuel_trims

if len(sys.argv) != 2:
    print "Usage: %s <logfile-directory>" % (os.path.basename(sys.argv[0]))
    sys.exit(0)

directory = sys.argv[1]

bands = rpm_bands.build_bands()

for filename in os.listdir(directory):
    for row in logfile.get_rows(directory + '/' + filename):
        fuel_trims.add_to_band(row, bands)

rpm_bands.print_bands(bands)
