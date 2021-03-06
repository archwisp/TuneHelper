#!/usr/bin/python #vim: ts=4:sw=4:et
import sys, os
from tunehelper import logfile, rpm_bands
import sqlite3

if len(sys.argv) != 2:
    print "Usage: %s <database-filename>" % (os.path.basename(sys.argv[0]))
    sys.exit(0)

db_filename = sys.argv[1]
dry_run = False
    
def get_records(db):
    cursor = db.cursor()
    return cursor.execute('''SELECT end_rpm, end_mph, ROUND(velocity_change,2), ROUND(duration,2) FROM logs WHERE velocity_change > 0 ORDER BY end_mph, end_rpm;''')
    
db = sqlite3.connect(db_filename)

first_gear = rpm_bands.buildBands() 
second_gear = rpm_bands.buildBands() 
third_gear = rpm_bands.buildBands() 
fourth_gear = rpm_bands.buildBands() 

# Tire Diameter: 25.6 in.
# 788 revs/mile

#  @ 9000 rpm
#  1st 3.815 40.4 
#  2nd 2.260 68.3
#  3rd 1.645 93.8
#  4th 1.177 131.1
#  5th 1.000 154.2
#  6th .832 185.4

# Final gear 4.44

for record in get_records(db):
    rpm = str(record[0] - (record[0] % 250))
    mph = record[1]
    accel = (record[2] * 0.445) / record[3]

    # trans ratio = (rpm * tire diam) / (mph * rear diff ratio * 336)
    trans_ratio = round((int(rpm) * 25.6) / (mph * 4.44 * 336),2)
   
    if trans_ratio > 3:
        first_gear[rpm].append(accel)
    elif trans_ratio > 2:
        second_gear[rpm].append(accel)
    elif trans_ratio > 1.1:
        third_gear[rpm].append(accel)
    elif trans_ratio > .9:
        fourth_gear[rpm].append(accel)
    
print "First Gear:\n"
rpm_bands.printBands(first_gear)

print "\nSecond Gear:\n"
rpm_bands.printBands(second_gear)

print "\nThird Gear:\n"
rpm_bands.printBands(third_gear)

print "\nFourth Gear:\n"
rpm_bands.printBands(fourth_gear)
