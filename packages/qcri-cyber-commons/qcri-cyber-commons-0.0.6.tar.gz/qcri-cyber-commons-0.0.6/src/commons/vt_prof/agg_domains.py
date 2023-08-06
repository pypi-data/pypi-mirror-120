'''
Description: aggreegate VT hosts for a given time period
'''
from datetime import date, timedelta, datetime
import sys
import os
#v3
#from urllib.parse import urlparse
#v27
from urlparse import urlparse
import fnmatch
import time
import tldextract

BASE_VT_DIR = "/export/sec04/vt/vt_url_feed_parsed_v2"

def get_vt(startdate, enddate):
    os.environ["TZ"] = "UTC"
    s_date = datetime.strptime(startdate.strip(), "%Y%m%d").date()
    e_date = datetime.strptime(enddate.strip(), "%Y%m%d").date()
    delta = e_date - s_date
    vt = dict()
    hosts = set()
    for i in range(delta.days + 1):
        curr_date = s_date + timedelta(i)
        name = "res.url-feed-{}T??".format(curr_date.strftime("%Y%m%d"))
        filenames = fnmatch.filter(os.listdir(BASE_VT_DIR), name)
        for filename in filenames:
            full_path = os.path.join(BASE_VT_DIR, filename)
            fo = open(full_path)
            for line in fo:
                #http://www.gorillawalker.com/my-blue-is-happy.pdf##2019-05-31 23:00:18##9bccab2dde30fcb77d7c91c3c6b1dabe188f3e3f00645de2722ce951494b5cd1-1559343618##5##CyRadar:malicious site#Avira:phishing site#Forcepoint ThreatSeeker:phishing site#Sophos:malicious site#Fortinet:phishing site
                arr = line.strip().split('##')
                if len(arr) != 5:
                    print("ERROR: Invalid line: {}".format(line))
                    continue
                url = arr[0]
                if url == None or len(url) == 0:
                    print("ERROR: Invalid URL: {}".format(line))
                    continue

                datestr = arr[1]
                try:
                    #epoch = int(time.mktime(datetime.strptime(datestr, "%Y-%m-%d %H:%M:%S").date().timetuple()))
                    epoch = int(datetime.strptime(datestr, '%Y-%m-%d %H:%M:%S').strftime('%s'))
                except Exception as e:
                    print("ERRROR - likely format issue: {}".format(line))
                    print(e)
                    pass
                    continue
                #scheme='https', netloc='ww.xy.com', path='/', params='', query='', fragment=''
                try:
                    uri = urlparse(url)
                    host = uri.netloc
                    ext = tldextract.extract(host)
                    domain = ext.domain + "." + ext.suffix
                except Exception as e:
                    print("ERROR - something went wrong while parsing the URL: {}".format(url))
                    print(e)
                    pass
                    continue


                if domain == None or len(domain) == 0:
                    print("ERROR: Invalid Domain: {}".format(line))
                    continue
                scan_id = arr[2]
                if scan_id == None or len(scan_id) == 0:
                    print("ERROR: Invalid scan id: {}".format(line))
                    continue

                if domain not in vt:
                    vt[domain] = dict()
                    vt[domain]['hosts'] = set()
                    vt[domain]['firstseen'] = epoch
                    vt[domain]['lastseen'] = epoch
                    vt[domain]['total'] = 0
                    vt[domain]['mal_count'] = 0

                vt[domain]['total'] += 1
                if int(arr[3]) > 0:
                    vt[domain]['mal_count'] += 1

                if vt[domain]['firstseen'] > epoch:
                    vt[domain]['firstseen'] = epoch

                if vt[domain]['lastseen'] < epoch:
                    vt[domain]['lastseen'] = epoch

                #postgres can't handle very large text fields - so summarize long host names
                if len(host) > 100:
                    host_str = "l0ngh0st." + str(len(host)) + "." + str(host.count('.'))
                    vt[domain]['hosts'].add(host_str)
                else:
                    vt[domain]['hosts'].add(host)
    print("#Domains = {}".format(len(vt)))
    count = 0
    for key, value in vt.items():
        count += 1
        if count == 5:
            break
        print("{}:{}".format(key, value))
    return vt
