from functools import reduce

def buildBands():
    bands = {
    }

    for band in range(0, 101, 5):
        bandobj = {str(band): []}
        bands.update(bandobj)

    return bands
    
def printBands(bands):
    for band in sorted(bands, key=int):
        if len(bands[band]) > 0:
            print("%s: %s" % (
                band, reduce(lambda x, y: x + y, bands[band]) / len(bands[band])
            ))

def compareBands(bands1, bands2):
    for band in sorted(bands1, key=int):
        if len(bands1[band]) > 0:
            band1 = reduce(lambda x, y: x + y, bands1[band]) / len(bands1[band])
            band2 = reduce(lambda x, y: x + y, bands2[band]) / len(bands2[band])
            
            print("%s: %s %s (%s %%)" % (
                band, round(band1,2), round(band2,2), round((1-(band1 / band2))*100, 2))
            )
