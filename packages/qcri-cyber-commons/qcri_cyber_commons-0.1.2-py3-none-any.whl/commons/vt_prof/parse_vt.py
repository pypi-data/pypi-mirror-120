import tarfile
import json
import glob
import sys
import os
import time
from urllib.parse import urlparse
from datetime import date, timedelta, datetime

BASE_VT_DIR = "/export/sec03/vt/vt_url_feed"
PARSED_VT_DIR = "/export/sec04/vt/vt_url_feed_parsed_v2"


def parse_vt_files(startdate, enddate):
    s_date = datetime.strptime(startdate.strip(), "%Y%m%d").date()
    e_date = datetime.strptime(enddate.strip(), "%Y%m%d").date()
    delta = e_date - s_date
    for i in range(delta.days + 1):
        curr_date = s_date + timedelta(i)
        files = glob.glob("{}/url-feed-{}T*.tar.bz2".format(BASE_VT_DIR, curr_date.strftime("%Y%m%d")))
        for fi in files:
            outf = "res.{0}".format(os.path.basename(fi).split('.')[0])
            extract_url_feed_tar(fi, os.path.join(PARSED_VT_DIR, outf))
            print("Parsed {}".format(os.path.basename(fi)))

def extract_url_feed_tar(fi, outf):
    fd = open(outf, "w+")
	
    try:
        tar = tarfile.open(fi, "r:bz2")
    except Exception as e:
        print(e)
        print("ERROR: parsing file {}".format(fi))
        return

    for item in tar:
        file_obj = tar.extractfile(item)
        if file_obj == None:
            continue

        for line in file_obj:
            try:
                url_obj = json.loads(line)
                url = url_obj["url"]
                scan_t = url_obj["scan_date"]
                scan_id = url_obj["scan_id"]
                positives = int(url_obj["positives"])
                avs = ""
                if positives > 0:
                    scans = url_obj['scans']
                    for av, result in scans.items():
                        if result["detected"] == True:
                            if len(avs) > 0:
                                avs += '#'
                            avs += av + ':' + result['result']
                fd.write("{}##{}##{}##{}##{}\n".format(url, scan_t, scan_id, positives, avs))
            except:
                print("ERROR: JSON object parsing error")       
                continue
    tar.close()
    fd.close()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print ("Usage: {} <startdate> <enddate>".format(sys.argv[0]))
        exit()
    parse_vt_files(sys.argv[1], sys.argv[2])
