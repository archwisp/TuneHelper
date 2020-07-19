def add_to_band(row, bands):
    # bands[str(row['rpm_band'])].append(row['afr'])
    if row['throttle'] > 40 and row['load'] > 80:
        bands[str(row['rpm_band'])].append(row['afr'])
