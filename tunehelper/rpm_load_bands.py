#vim: ts=4:sw=4:et
from functools import reduce
import rpm_bands

def buildBands():
    load_bands = {}
    for load_band in range(0, 105, 5):
        bandobj = {str(load_band): []}
        load_bands.update(bandobj)
    
    rpm_load_bands = rpm_bands.buildBands()
    
    for rpm_band in rpm_load_bands:
        rpm_load_bands[rpm_band] = load_bands

    return rpm_load_bands

def compareBands(bands1, bands2):
    for rpm in sorted(bands1, key=int):
        for load in sorted(bands1[rpm], key=int):
            if len(bands1[rpm]) > 0:
                rpm_load1 = reduce(lambda x, y: x + y, bands1[rpm][load]) / len(bands1[rpm][load])
                rpm_load2 = reduce(lambda x, y: x + y, bands2[rpm][load]) / len(bands2[rpm][load])
                
                print("RPM: %s Load: %s: %s %s (%s %%)" % (
                    rpm, load, 
                    round(rpm_load1,2), round(rpm_load2,2), round((1-(rpm_load1 / rpm_load2))*100, 2))
                )
