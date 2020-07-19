#vim: ts=4:sw=4:et
from functools import reduce
import logfile

# Closed loop conditions
# Max RPM 6000
# Max throttle 60% under 3000 RPM or 70%
# Max load
    # 100% under 2500 RPM
    # 75.7% @ 2500
    # 65.9% @ 3000
    # 47.1% @ 3500
    # 28.2% @ 4000
    # 25.1% up to 5500

def isClosedLoop(row):
    if row['rpm'] > 6000:
        return False;

    if row['throttle'] > 70:
        return False;

    if row['rpm'] < 3000 and row['throttle'] > 60:
        return False;
  
    if row['rpm'] >= 5490 and row['load'] >= 25.1:
        return False;
    
    if row['rpm'] >= 4000 and row['load'] >= 28.2:
        return False;
    
    if row['rpm'] >= 3500 and row['load'] >= 47.1:
        return False;
    
    if row['rpm'] >= 3000 and row['load'] >= 69.5:
        return False;
    
    if row['rpm'] >= 2500 and row['load'] >= 75.7:
        return False;

    return True

def isLean(prev_row, row):
    # Not warmed up yet
    # if row['ect'] < 70:
        # return False

    # Maxed out sensor / throttle lift
    if row['afr'] > 1.3 and row['stft'] == 0:
        return False;

        # return False
    
    # Getting rolling
    if row['speed'] <= 10:
        return False
    
    # Probably throttle lift
    if row['throttle'] <= 25:
        return False
   
    # Leaning out during lift is normal
    if prev_row != "":
        if  prev_row['load'] > row['load']:
            return False

        if prev_row['throttle'] > row['throttle']:
            return False
    
        if prev_row['speed'] > row['speed']:
            return False
        
        if prev_row['rpm'] > row['rpm']:
            return False

    if row['afr_diff'] < 3:
        return False

    if not isClosedLoop(row):
        return False

    return True

def isRich(row):
    if isClosedLoop(row) and row['afr_diff'] < -3: # and row['afr'] < 0.80:
        return True
    else:
        return False

def addToRpmLoadBand(row, target_afr_bands, afr_bands):
    target_afr_bands[str(row['rpm_band'])][str(row['load_band'])].append(row['target_afr'])
    afr_bands[str(row['rpm_band'])][str(row['load_band'])].append(row['afr'])

def addToLoadBand(row, target_afr_bands, afr_bands):
    target_afr_bands[str(row['load_band'])].append(row['target_afr'])
    afr_bands[str(row['load_band'])].append(row['afr'])
