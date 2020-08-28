#!/usr/bin/python #vim: ts=4:sw=4:et
import sys, os
from tunehelper import logfile
import csv
import sqlite3

# SELECT count(*), round(end_mph), end_rpm - (end_rpm % 100) as end_rpm, avg(velocity_change) from logs WHERE (start_rpm - (start_rpm % 100) <> end_rpm - (end_rpm % 100)) GROUP BY start_mph, end_mph, start_rpm - (start_rpm % 100), end_rpm - (end_rpm % 100);
# SELECT round(end_mph), end_rpm - (end_rpm % 100) as end_rpm, avg(velocity_change) from logs WHERE (start_rpm - (start_rpm % 100) <> end_rpm - (end_rpm % 100)) GROUP BY start_mph, end_mph, start_rpm - (start_rpm % 100), end_rpm - (end_rpm % 100) ORDER BY end_mph, end_rpm;
# SELECT round(end_mph), end_rpm - (end_rpm % 100) as end_rpm, avg(velocity_change) from logs WHERE (start_rpm - (start_rpm % 100) <> end_rpm - (end_rpm % 100)) and velocity_change > 0 GROUP BY start_mph, end_mph, start_rpm - (start_rpm % 100), end_rpm - (end_rpm % 100) ORDER BY end_mph, end_rpm;

def init_db(db):
    cursor = db.cursor()
    cursor.execute('''DROP TABLE IF EXISTS logs''')
    cursor.execute('''CREATE TABLE logs (start_rpm int, end_rpm int, start_mph int, end_mph int, duration float, velocity_change float)''')

def insert_to_db(db, start_rpm, end_rpm, start_mph, end_mph, duration, velocity_change):
    cursor = db.cursor()
    cursor.executemany('''INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?)''', [(start_rpm, end_rpm, start_mph, end_mph, duration, velocity_change)])

# Acceleration = velocity change / time
def acceleration_from_speed(velocity_change, duration):
    return (velocity_change * 0.445) / duration

# Force = mass * accelleration
# Power = force * speed
def horsepower_from_acceleration(weight, acceleration_m_s_2, avg_velocity):
    mass_kg = weight * 0.453592
    force_n = mass_kg * acceleration_m_s_2
    avg_velocity_m_s = avg_velocity * 0.454
    power = force_n * avg_velocity_m_s
    return power / 745.7

def print_current_run_summary(current_run):
    if (len(current_run["velocity"]) > 0):
        avg_velocity = sum(current_run["velocity"]) / len(current_run["velocity"])
        velocity_change = sum(current_run["velocity_change"]) 
        duration = sum(current_run["duration"]) 

        if (velocity_change > 10):

            acceleration_m_s_2 = acceleration_from_speed(velocity_change, duration)
            horsepower = horsepower_from_acceleration(3200, acceleration_m_s_2, avg_velocity) 
        
            print "Speed: %s-%s RPM: %s-%s, Velocity Change: %s Duration: %s Avg. Acceleration (m/s2): %s Avg. Horsepower: %s" % (
                str(round(min(current_run["velocity"]))), 
                str(round(max(current_run["velocity"]))), 
                str(min(current_run["rpm"])), 
                str(max(current_run["rpm"])), 
                str(round(velocity_change, 2)).ljust(6), 
                str(round(duration, 2)).ljust(6), 
                str(round(acceleration_m_s_2, 2)).ljust(6),
                str(int(horsepower)).ljust(6)
            )

if len(sys.argv) != 3:
    print "Usage: %s <logfile-directory> <database-filename>" % (os.path.basename(sys.argv[0]))
    sys.exit(0)

directory = sys.argv[1]
db_filename = sys.argv[2]
dry_run = False

print "Processing directory: %s" % directory

if not dry_run:
    db = sqlite3.connect(db_filename)
    init_db(db)

for root, subdirs, files in os.walk(directory):
    for filename in files:
        filename = os.path.join(root, filename)
        
        print "Processing file: %s" % filename

        run = 1
        sample_counter = 1
        last_row = None
        acceleration = 0
        current_run = {"duration": [], "velocity_change": [], "velocity": [], "rpm": []} 

        for row in logfile.getRows(filename):
            if isinstance(row, Exception):
                break

            if row['throttle'] == 78 and row['load'] > 95: 
                if last_row != None:
                    if row['sample'] != (last_row['sample'] + 1) or row['rpm'] < last_row['rpm']:
                        print_current_run_summary(current_run)
                        sample_counter = 1
                        run += 1

                if sample_counter == 1:
                    current_run = {"duration": [], "velocity_change": [], "velocity": [], "rpm": []} 
               
                # Skip the first record becuase we can't calculate anything with no
                # previous record

                if sample_counter > 1:
                    duration = row['time'] - last_row['time']
                    velocity_change = row['speed'] - last_row['speed'] 
                    avg_velocity = (row['speed'] + last_row['speed']) / 2
                    acceleration_m_s_2 = acceleration_from_speed(velocity_change, duration)
                    horsepower = horsepower_from_acceleration(3200, acceleration_m_s_2, avg_velocity) 

                    current_run["duration"].append(duration)
                    current_run["velocity_change"].append(velocity_change)
                    current_run["velocity"].append(row["speed"])
                    current_run["rpm"].append(row["rpm"])

                    insert_to_db(db, 
                        start_rpm=last_row["rpm"], end_rpm=row["rpm"],
                        start_mph=last_row["speed"], end_mph=row["speed"],
                        duration=duration, velocity_change=velocity_change
                    )
                
                sample_counter += 1
                last_row = row
        
        print_current_run_summary(current_run)

db.commit()
db.close()
