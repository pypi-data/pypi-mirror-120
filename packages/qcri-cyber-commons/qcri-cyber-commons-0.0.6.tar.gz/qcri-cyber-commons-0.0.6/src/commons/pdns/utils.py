'''
Description: utility functions
Author: @nabeelxy 
'''
from datetime import datetime
import tldextract
import time

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

#get the TLD of a given FQDN (e.g. mail.qcri.org --> qcri.org, www.bbc.co.uk --> bbc.co.uk)
def get_2ld(fqdn):
  ext = tldextract.extract(fqdn)
  return ext.domain + "." + ext.suffix

def get_all_tlds(domain_file, outfile):
    twolds = set()
    with open(domain_file) as df:
        for domain in df:
            domain = domain.strip()
            twolds.add(get_2ld(domain))
    of = open(outfile, "w+")
    for twold in twolds:
        of.write("{}\n".format(twold))
    of.close()
