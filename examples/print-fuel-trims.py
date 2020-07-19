#!/usr/bin/python #vim: ts=4:sw=4:et
import sys, os
from tunehelper import logfile, rpm_bands, fuel_trims, afrs

if len(sys.argv) != 2:
    print "Usage: %s <logfile-directory>" % (os.path.basename(sys.argv[0]))
    sys.exit(0)

directory = sys.argv[1]

stft_bands = rpm_bands.buildBands()
ltft_bands = rpm_bands.buildBands()

for filename in os.listdir(directory):
    for row in logfile.getRows(directory + '/' + filename):
        if afrs.isClosedLoop(row):
            fuel_trims.addToBand(row, stft_bands, ltft_bands)

print("STFT")
rpm_bands.printBands(stft_bands)
print("\nLTFT")
rpm_bands.printBands(ltft_bands)
