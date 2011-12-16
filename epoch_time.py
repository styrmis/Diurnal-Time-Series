# The functions below are not at present used for the diurnal calculations
# however may be of use as the data this script is designed for uses
# epoch time (starting January 1, 1904).

SECONDS_IN_DAY = 60 * 60 * 24

def epoch_day_number(epoch_time):
    int(math.floor(float(epoch_time) / SECONDS_IN_DAY))

def epoch_in_same_day(e1, e2):
    return epoch_day_number(e1) == epoch_day_number(e2)

def normalise_to_start_of_day(dt):
    "Given a datetime object for a time like 16:42:53 this will return 00:00:00 for that day"
    return dt - timedelta(hours=dt.hour, minutes=dt.minute, seconds=dt.second)

def normalise_to_start_of_minute(dt):
        "Given a datetime object for a time like 16:42:53 this will return 16:42:00"
        return dt - timedelta(seconds=dt.second)