from datetime import datetime
import os
from datetime import date, timedelta

os.environ["TZ"] = "UTC"

def get_dt(dstr, dformat = "%b %d %Y %I:%M %p"):
    dstr = dstr.replace("th", "").replace("st", "").replace("nd", "").replace("rd", "")
    return datetime.strptime(dstr, dformat)

def epoch2dt(epoch, dformat = "%Y-%m-%dT%H:%M:%S.%fZ"):
    return datetime.fromtimestamp(epoch).strftime(dformat) #'%Y-%m-%d %H:%M:%S')

def ts2dt(ts, dformat = "%Y-%m-%dT%H:%M:%S.%fZ"):
    return datetime.strptime(ts, dformat) #'%Y-%m-%d %H:%M:%S'

def dt2epoch(dt):
    return dt.timestamp()

#get duration in days
def get_duration(row):
    return (ts2dt(row["lastseen"]).timestamp() - ts2dt(row["firstseen"]).timestamp())/86400

def dt2str(dt, dformat = "%Y-%m-%dT%H:%M:%S.%fZ"):
    return dt.strftime(dformat)


##specific to VT
# handle multiple dateformats in VT historical whois and conver to epoch time
def vtdate2epoch(datestr):
    date_formats = ["%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S.%fZ", "%d-%b-%Y %H:%M:%S",
               "%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d.%m.%Y %H:%M:%S", "%d/%m/%Y %H:%M:%S",
               "%Y-%m-%d %H:%M:%S%z", "%d-%b-%Y", "%Y-%m-%d %H:%M:%S.%f", "%Y%m%d",
               "%d.%m.%Y", "%B %d %Y", "%Y-%m-%dT%H:%M:%S.%f", "%a, %d %b %Y %H:%M:%S",
                "%Y.%m.%d %H:%M:%S" ]
    epoch = None
    
    if datestr != None and datestr != "" and datestr != float:
        ds = [datestr]
        if "|" in datestr:
            ds = [x.strip() for x in datestr.split("|")]
        for dformat in date_formats:
            found = False
            
            for d in ds:
                #exclude +02, +03  etc.
                try:
                    plus = d.index("+")
                    d = d[0:plus]
                except ValueError as e:
                    pass
                try:
                    utc = d.index("UTC")
                    d = d[0:utc].strip()
                except ValueError as e2:
                    pass

                try:
                    epoch = dt2epoch(ts2dt(d, dformat))
                    found = True
                    break
                except:
                    pass
            if found == True:
                break
        if found == False:
            print(datestr)
    return epoch
