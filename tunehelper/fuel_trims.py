#vim: ts=4:sw=4:et
def addToBand(row, stft_bands, ltft_bands):
    if row['throttle'] > 25 and row['rpm'] < 4500:
        stft_bands[str(row['rpm_band'])].append(row['stft'])
        ltft_bands[str(row['rpm_band'])].append(row['ltft'])

