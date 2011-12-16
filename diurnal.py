#!/usr/bin/env python

# Run this script like this: python diurnal.py data.csv

import sys
import datetime
from datetime import timedelta
import csv
import math

# This value will get filled in for any missing values in the data
MISSING_VALUE = 'nan'

class DataPoint(object):
    def __init__(self, epoch_time, value):
        self.epoch_time = epoch_time
        self.value = value
    
    def get_as_datetime(self):
        "Convert from 1904 Epoch time to regular datetime object"
        midnight_jan_1_1904 = datetime.datetime(1904, 1, 1, 0, 0, 0)
        return midnight_jan_1_1904 + timedelta(seconds=self.epoch_time)
    datetime = property(get_as_datetime)

    def normalise_to_start_of_day(self):
        "Given a datetime object for a time like 16:42:53 this will return 00:00:00 for that day"
        return self.datetime - timedelta(hours=self.datetime.hour, minutes=self.datetime.minute, seconds=self.datetime.second)

    def normalise_to_start_of_hour(self):
        "Given a datetime object for a time like 16:42:53 this will return 16:00:00"
        return self.datetime - timedelta(minutes=self.datetime.minute, seconds=self.datetime.second)

    def normalise_to_start_of_minute(self):
        "Given a datetime object for a time like 16:42:53 this will return 16:42:00"
        return self.datetime - timedelta(seconds=self.datetime.second)

# If running from the terminal, the code below will be run
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: %s <path_to_csv_file>" % sys.argv[0]
        sys.exit(1)
    
    csv_file_path = sys.argv[1]
    
    reader = csv.reader(open(csv_file_path, 'rU'), delimiter='\t')
    
    # Skip the first row, it's just column headers
    reader.next()
    
    data_points = []
    
    minutes = {}
    
    for row in reader:
        # Extract epoch time and data point
        epoch_time = int(row[0])
        value = row[1]
        
        data_point = DataPoint(epoch_time, value)
        data_points.append(data_point)
        
        minutes.setdefault(data_point.normalise_to_start_of_minute(), {})
        minutes[data_point.normalise_to_start_of_minute()][data_point.normalise_to_start_of_day()] = data_point
    
    # Data must already be sorted for this to be correct
    lowest_date = data_points[0].datetime
    highest_date = data_points[-1].datetime
    
    start_of_first_day = lowest_date - timedelta(hours=lowest_date.hour, minutes=lowest_date.minute, seconds=lowest_date.second)
    end_of_last_day = highest_date - timedelta(hours=highest_date.hour, minutes=highest_date.minute+1, seconds=highest_date.second) + timedelta(days=1)
    
    print "Range found in data:", lowest_date, highest_date
    print "Expanded range used for output:", start_of_first_day, end_of_last_day
    
    days = []
    
    current_day = start_of_first_day
    
    while current_day <= end_of_last_day:
        days.append(current_day)
        current_day += timedelta(days=1)
    
    # This will be 24 * 60 = 1440 long, one row per minute in the day
    minutes_list = []
    
    for min_number in xrange(24 * 60):
        day_list = []
        
        for day in days:
            that_minute_on_this_day = day + timedelta(minutes=min_number)
            
            if minutes.has_key(that_minute_on_this_day) and minutes[that_minute_on_this_day].has_key(day):
                day_list.append(minutes[that_minute_on_this_day][day].value)
            else:
                day_list.append(MISSING_VALUE)
        
        minutes_list.append(day_list)
    
    writer = csv.writer(open('output.csv', 'w'))
    
    writer.writerow([ d.strftime('%d/%m/%y') for d in days ])
    
    writer.writerows(minutes_list)
    
    writer = csv.writer(open('output_t.csv', 'w'))
    
    writer.writerows(zip(*minutes_list))
        