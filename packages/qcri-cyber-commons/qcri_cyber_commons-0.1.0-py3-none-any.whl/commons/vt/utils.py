import os
from datetime import datetime

os.environ["TZ"] = "UTC"

# get the current date in YYYYMMDD format
# note: no validation
def get_current_date():
    return str(datetime.now().strftime("%Y%m%d"))

def get_current_time_epoch():
    return time.mktime(datetime.now().timetuple())

# get the date object for a date string of the format YYYYMMDD
# note that no validation is performed here; so make sure to
# pass the date in the correct format
def get_date_obj(date_str):
    return datetime.strptime(date_str, "%Y%m%d").date()

def validate_date(date_text):
    try:
        get_date_obj(date_text)
    except ValueError:
        raise ValueError("Invalid date format, should be YYYY-MM-DD")

def date2epoch(datestr, dformat = '%Y-%m-%dT%H:%M:%SZ'): #dformat = '%Y%m%d %H:%M'):
    return int(datetime.strptime(datestr, dformat).strftime('%s'))

def epoch2datestr(ts_epoch, dformat = '%Y%m%d %H:%M'):
    return datetime.utcfromtimestamp(ts_epoch).strftime(dformat)
