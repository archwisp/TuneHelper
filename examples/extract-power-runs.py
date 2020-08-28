#!/usr/bin/python #vim: ts=4:sw=4:et
import sys, os
from tunehelper import logfile
import csv

if len(sys.argv) != 3:
    print "Usage: %s <logfile-directory> <output-directory>" % (os.path.basename(sys.argv[0]))
    sys.exit(0)

directory = sys.argv[1]
output_directory = sys.argv[2]
dry_run = False

print "Processing directory: %s" % directory

if not dry_run:
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

for filename in os.listdir(directory):
    run = 1
    sample_counter = 1
    last_row = None
    try:
        rows = logfile.getRows(directory + '/' + filename)
    except:
        next

    for row in rows:
        if row['throttle'] == 78 and row['load'] > 95: 
            if last_row != None:
                if row['sample'] != (last_row['sample'] + 1) or row['rpm'] < last_row['rpm']:
                    sample_counter = 1
                    run += 1

            if sample_counter == 1:
                print "Run: %s" % run

                if not dry_run:
                    outfile = output_directory + '/' + filename[:-4] + '_run' + str(run) + '.csv'
                    wr = csv.writer(open(outfile, "w"), delimiter=",")
                    
                    wr.writerow([
                        'sample', 'time', 'Throttle', 'SpeedMPH', 'RPM',
                        'CalcLoad', 'MAFVolts', 'STFT', 'LTFT', 'IAT',
                        'ECT', 'AFR', 'TargetAFR', 'CatTemp'
                    ])
           
            logfile.printRow(filename, row)

            if not dry_run:
                wr.writerow([
                    str(sample_counter),
                    str(row['time']),
                    str(row['throttle']),
                    str(row['speed']),
                    str(row['rpm']),
                    str(row['load']),
                    str(row['maf_volts']),
                    str(row['stft']),
                    str(row['ltft']),
                    str(row['iat']),
                    str(row['ect']),
                    str(row['afr']),
                    str(row['target_afr']),
                    str(row['cat'])
                ])
            
            sample_counter += 1
            last_row = row
