#vim: ts=4:sw=4:et
import sys, csv

# MEP Fields
# ==========
# Time
# Calculated Engine Load (OBD) (%)
# Commanded Air/Fuel Ratio (OBD) (AFR)
# Engine coolant Temperature (C)
# Absolute Engine Load (OBD) (%)
# Air Conditioning Compressor Cycling Switch
# Air/Fuel S1 Current (OBD) (mA)
# Intake Air Temperature (OBD) (C)
# Mass Airflow Sensor (Volts)
# Vehicle Speed (OBD) (mph)
# Fuel Status 1 (bit)
# Generator Voltage Desired (Volts)
# Ignition Timing (OBD) (CA)
# Fuel Pulse Width (mS)
# Ambient Air Temperature (OBD) (C)
# Catalyst Temperature B1S1 (C)
# Idle Air Control (%)
# Intake Air Shutter Valve switch (?on/off)
# Engine Speed (OBD) (RPM)
# Air/Fuel Ratio S1 E2 (OBD) (AFR)
# Absolute Throttle Position (OBD) (%)
# Generator Output Voltage (Volts)
# A/C Request Signal
# Short Term Fuel Trim B1 (OBD) (%)
# Long Term Fuel Trim B1 (OBD) (%)

def getMazdaEditHeaderMap(header):
    header_map = {
            'afr': header.index("Air/Fuel Ratio S1 E2 (OBD) (AFR)"),
            'cat': header.index("Catalyst Temperature B1S1 (C)"),
            'ect': header.index("Engine coolant Temperature (C)"),
            'iat': header.index("Intake Air Temperature (OBD) (C)"),
            'load': header.index("Calculated Engine Load (OBD) (%)"),
            'ltft': header.index("Long Term Fuel Trim B1 (OBD) (%)"),
            # 'maf': header.index(""),
            'maf_volts': header.index("Mass Airflow Sensor (Volts)"),
            'rpm': header.index("Engine Speed (OBD) (RPM)"),
            'speed': header.index("Vehicle Speed (OBD) (mph)"),
            'stft': header.index("Short Term Fuel Trim B1 (OBD) (%)"),
            'target_afr': header.index("Commanded Air/Fuel Ratio (OBD) (AFR)"),
            'throttle': header.index("Absolute Throttle Position (OBD) (%)"),
            'time': header.index("Time"),
            }

    return header_map

def getTactrixHeaderMap(header):
    header_map = {
            'afr': header.index("AFR"),
            'cat': header.index("CatTemp"),
            'ect': header.index("ECT"),
            'iat': header.index("IAT"),
            'load': header.index("CalcLoad"),
            'ltft': header.index("LTFT"),
            # 'maf': header.index("MAF"),
            'maf_volts': header.index("MAFVolts"),
            'rpm': header.index("RPM"),
            'speed': header.index("SpeedMPH"),
            'stft': header.index("STFT"),
            'target_afr': header.index("TargetAFR"),
            'throttle': header.index("Throttle"),
            'time': header.index("time"),
            }

    return header_map

def getRows(filename):
    if filename.endswith(".csv"):
        rows = csv.reader(open(filename, "r"), delimiter=",")
        header = next(rows)
   
        try:
            if (filename.find("mazdaEdit") >= 0):
                header_map = getMazdaEditHeaderMap(header)
            else:
                header_map = getTactrixHeaderMap(header)
        except ValueError as error:
            print("Failed to map headers for %s: %s" % (filename, error))
            return
            
        for row in rows:
            try:
                float(row[header_map['time']])
            except ValueError:
                header_map = getMazdaEditHeaderMap(row)
                continue

            throttle = int(round(float(row[header_map['throttle']]), 2))
            rpm = int(round(float(row[header_map['rpm']]), 0))
            load = int(round(float(row[header_map['load']]), 2))
            stft = round(float(row[header_map['stft']]), 2)
            ltft = round(float(row[header_map['ltft']]), 2)
            trim = stft + ltft
            afr_diff = int(round(float(row[header_map['afr']]) - float(row[header_map['target_afr']]), 2) * 100)
        
            rowobj = {
                'afr': round(float(row[header_map['afr']]), 2),
                'afr_diff': afr_diff,
                'cat': int(round(float(row[header_map['cat']]), 3)),
                'ect': int(row[header_map['ect']]),
                'iat': int(row[header_map['iat']]),
                'load': load,
                'load_band': load - (load % 5),
                # 'maf': row[header_map['maf']],
                'maf_volts': round(float(row[header_map['maf_volts']]), 2),
                'ltft': ltft,
                'ltr': load - throttle,
                'rpm': rpm,
                'rpm_band': rpm - (rpm % 250),
                'speed': int(round(float(row[header_map['speed']]), 0)),
                'stft': stft,
                'target_afr': round(float(row[header_map['target_afr']]), 2),
                'throttle': throttle,
                'time': round(float(row[header_map['time']]), 2),
                'trim': trim,
            }

            yield rowobj 

def printRow(filename, row):
    ect = row['ect']
    ect_f = int(ect * 1.8 + 32)
    cat = row['cat'] 
    cat_f = int(cat * 1.8 + 32)

    print("File: %s  Time: %s  Throttle: %s  Load: %s  Speed: %s  RPM: %s TragetAFR: %s  AFR: %s  Diff %%: %s  LTFT: %s  STFT: %s  ECT: %sC/%sF Cat: %sC/%sF" % (
        filename, 
        str(row['time']).ljust(10), 
        str(row['throttle']).ljust(2), 
        str(row['load_band']).ljust(3), 
        str(row['speed']).ljust(3), 
        str(row['rpm_band']).ljust(4), 
        str(row['target_afr']).ljust(4), 
        str(row['afr']).ljust(4), 
        str(row['afr_diff']).ljust(2), 
        str(row['ltft']).ljust(5), 
        str(row['stft']).ljust(5), 
        str(ect).ljust(2), 
        str(ect_f).ljust(3), 
        str(cat).ljust(3), 
        str(cat_f).ljust(4), 
        ))
