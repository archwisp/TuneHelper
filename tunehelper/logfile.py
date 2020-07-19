import csv

def get_rows(filename):
    if filename.endswith(".csv"):
        rows = csv.reader(open(filename, "r"), delimiter=",")
        rows.next() # Skip header row
            
        for row in rows:
        
            # 0:sample, 1:time, 2:Throttle, 3:SpeedMPH, 4:RPM,
            # 5:CalcLoad, 6:MAFVolts, 7:MAF, 8:STFT, 9:LTFT, 
            # 10:IAT, 11:ECT, 12:AFR, 13:TargetAFR, 14:CatTemp
    
            throttle = int(round(float(row[2]), 2))
            rpm = int(round(float(row[4]),0))
            load = int(round(float(row[5]), 2))

            rowobj = {
                'sample': int(row[0]),
                'time': float(row[1]),
                'throttle': throttle,
                'speed': int(round(float(row[3]), 0)),
                'rpm': rpm,
                'rpm_band': rpm - (rpm % 250),
                'load': load,
                'load_band': load - (load % 5),
                'maf_volts': round(float(row[6]), 3),
                'maf': round(float(row[7]), 3),
                'stft': float(row[8]),
                'ltft': float(row[9]),
                'trim': float(row[8]) + float(row[9]),
                'iat': float(row[10]),
                'ect': float(row[11]),
                'afr': round(float(row[12]), 3),
                'target_afr': round(float(row[13]), 3),
                'cat': int((round(float(row[14]), 3) * 1.8) + 32),
                'ltr': load - throttle
            }

            yield rowobj 
