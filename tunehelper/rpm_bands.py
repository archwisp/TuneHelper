def build_bands():
    bands = {
    }

    for band in range(0, 9001, 250):
        bandobj = {str(band): []}
        bands.update(bandobj)

    return bands
    
def print_bands(bands):
    for band in sorted(bands, key=int):
        if len(bands[band]) > 0:
            print "%s: %s" % (
                band, reduce(lambda x, y: x + y, bands[band]) / len(bands[band])
            )
