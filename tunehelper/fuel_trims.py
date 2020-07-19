def add_to_band(row, bands):
    if row['throttle'] > 25 and row['rpm'] < 4500:
        bands[str(row['rpm_band'])].append(row['trim'])

