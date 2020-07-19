#!/usr/bin/python #vim: ts=4:sw=4:et
import sys, os
from tunehelper import logfile, rpm_bands, afrs, load_bands

if len(sys.argv) != 2:
    print "Usage: %s <logfile-directory>" % (os.path.basename(sys.argv[0]))
    sys.exit(0)

directory = sys.argv[1]
target_afr_bands = load_bands.buildBands()
afr_bands = load_bands.buildBands()

for filename in os.listdir(directory):
    for row in logfile.getRows(directory + '/' + filename):
        if not afrs.isClosedLoop(row):
            afrs.addToLoadBand(row, target_afr_bands, afr_bands)

# print("Target AFR")
# rpm_bands.printBands(target_afr_bands)
# print("\nAFR")
# rpm_bands.printBands(afr_bands)

load_bands.compareBands(target_afr_bands, afr_bands)
