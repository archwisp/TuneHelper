#!/usr/bin/python
import sys, os
from tunehelper import logfile
import csv


if len(sys.argv) != 3:
    print "Usage: %s <logfile-directory> <output-directory>" % (os.path.basename(sys.argv[0]))
    sys.exit(0)

directory = sys.argv[1]
output_directory = sys.argv[2]

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

for filename in os.listdir(directory):
    run = 1
    sample_counter = 1
    last_file_sample = 0
    
    for row in logfile.get_rows(directory + '/' + filename):
        if row['throttle'] == 78 and row['load'] > 95 and row['rpm'] > 5500 and row['speed'] > 60:
            
            if last_file_sample != 0 and row['sample'] -1 != last_file_sample:
                sample_counter = 1
                run += 1
            
            if sample_counter == 1:
                outfile = output_directory + '/' + filename[:-4] + '_run' + str(run) + '.csv'
                wr = csv.writer(open(outfile, "w"), delimiter=",")

                wr.writerow([
                    'sample', 'time', 'Throttle', 'SpeedMPH', 'RPM',
                    'CalcLoad', 'MAFVolts', 'MAF', 'STFT', 'LTFT', 'IAT',
                    'ECT', 'AFR', 'TargetAFR', 'CatTemp'
                ])

            print "File: %s Run: %s  Sample: %s  Time: %s  Throttle: %s  Load: %s  Speed: %s  RPM: %s  AFR: %s  Cat: %s F" % (
                filename, 
                str(run), 
                str(row['sample']).ljust(6), 
                str(row['time']).ljust(10), 
                str(row['throttle']).ljust(3), 
                str(row['load_band']).ljust(3), 
                str(row['speed']).ljust(3), 
                str(row['rpm_band']).ljust(4), 
                str(row['afr']).ljust(5), 
                str(row['cat']).ljust(4)
            )

            wr.writerow([
                str(sample_counter),
                str(row['time']),
                str(row['throttle']),
                str(row['speed']),
                str(row['rpm']),
                str(row['load']),
                str(row['maf_volts']),
                str(row['maf']),
                str(row['stft']),
                str(row['ltft']),
                str(row['iat']),
                str(row['ect']),
                str(row['afr']),
                str(row['target_afr']),
                str(row['cat'])
            ])
            
            last_file_sample = row['sample']
            sample_counter += 1
