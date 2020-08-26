#!/usr/bin/python #vim: ts=4:sw=4:et
import sys, os
from tunehelper import logfile
import csv

def acceleration_from_speed(velocity_change, duration):
    return (velocity_change * 0.445) / duration

def horsepower_from_acceleration(weight, acceleration_m_s_2, avg_velocity):
    mass_kg = weight * 0.453592
    force_n = mass_kg * acceleration_m_s_2
    avg_velocity_m_s = avg_velocity * 0.454
    power = force_n * avg_velocity_m_s
    return power / 745.7

if len(sys.argv) != 3:
    print "Usage: %s <logfile-directory> <output-directory>" % (os.path.basename(sys.argv[0]))
    sys.exit(0)

directory = sys.argv[1]
output_directory = sys.argv[2]
dry_run = True

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

for filename in os.listdir(directory):
    run = 1
    sample_counter = 1
    last_row = None
    acceleration = 0
    runs = []

    for row in logfile.getRows(directory + '/' + filename):
        if row['throttle'] == 78 and row['load'] > 95 and row['rpm'] > 2000: 
            if last_row != None:
                if row['sample'] != (last_row['sample'] + 1) or row['rpm'] < last_row['rpm']:
                    sample_counter = 1
                    run += 1

            if sample_counter == 1:
                print "Run: %s" % run
                runs.append({"time":"", "acceleration":"speed"})
            
                if not dry_run:
                    outfile = output_directory + '/' + filename[:-4] + '_run' + str(run) + '.csv'
                    wr = csv.writer(open(outfile, "w"), delimiter=",")
                    
                    wr.writerow([
                        'sample', 'time', 'Throttle', 'SpeedMPH', 'RPM',
                        'CalcLoad', 'MAFVolts', 'STFT', 'LTFT', 'IAT',
                        'ECT', 'AFR', 'TargetAFR', 'CatTemp'
                    ])
           
            # Acceleration = velocity change / time
            # Force = mass * accelleration
            # Power = force * speed
       
            # Skip the first record becuase we can't calculate anything with no
            # previous record

            if sample_counter > 1:
                duration = row['time'] - last_row['time']
                velocity_change = row['speed'] - last_row['speed'] 
                avg_velocity = (row['speed'] + last_row['speed']) / 2
                acceleration_m_s_2 = acceleration_from_speed(velocity_change, duration)
                horsepower = horsepower_from_acceleration(3200, acceleration_m_s_2, avg_velocity) 

                print "RPM: %s Speed (mph): %s Velocity Change: %s  Time: %s Acceleration (m/s2): %s Horsepower: %s" % (
                    str(row['rpm']).ljust(6), 
                    str(row['speed']).ljust(6), 
                    str(round(velocity_change, 2)).ljust(6), 
                    str(round(duration, 2)).ljust(6), 
                    str(round(acceleration_m_s_2, 2)).ljust(6),
                    str(int(horsepower)).ljust(6)
                )
                
                #  print "RPM: %s Prvious Velocity (mph): %s Velocity (mph): %s Time: %s Acceleration (m/s): %s Force (N) %s Avg Velocity (m/s): %s Watts: %s Horsepower: %s" % (
                    #  str(row['rpm']).ljust(6), 
                    #  str(previous_speed).ljust(6), 
                    #  str(row['speed']).ljust(6), 
                    #  str(duration).ljust(6), 
                    #  str(round(acceleration_m_s_2, 2)).ljust(6),
                    #  str(int(force_n)).ljust(6),
                    #  str(round(avg_velocity_m_s, 2)).ljust(6),
                    #  str(int(power)).ljust(6),
                    #  str(int(horsepower)).ljust(6)
                #  )

            # logfile.printRow(filename, row)

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
            
