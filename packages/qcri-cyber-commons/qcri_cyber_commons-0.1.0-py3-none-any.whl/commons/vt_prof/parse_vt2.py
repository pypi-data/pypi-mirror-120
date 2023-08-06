#Compared to parse_vt - this adds the IP as well
import tarfile
import json
import glob
import sys
import os
import time
from urllib.parse import urlparse
from datetime import date, timedelta, datetime

BASE_VT_DIR = "/export/sec03/vt/vt_url_feed"
PARSED_VT_DIR = "/export/sec04/vt/vt_url_feed_parsed_v3"


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

def write_record(fd, record):
    try:
        url_obj = json.loads(record)
        url = url_obj["url"]
        scan_t = url_obj["scan_date"]
        scan_id = url_obj["scan_id"]
        positives = int(url_obj["positives"])
        ip = "NONE"
        try:
            ip = url_obj["additional_info"]["resolution"]
        except:
            pass
        avs = ""
        if positives > 0:
            scans = url_obj['scans']
            for av, result in scans.items():
                if result["detected"] == True:
                    if len(avs) > 0:
                        avs += '#'
                    avs += av + ':' + result['result']
        fd.write("{}##{}##{}##{}##{}##{}\n".format(url, scan_t, scan_id, positives, avs, ip))
    except Exception as e:
        print(e)
        print("ERROR: JSON object parsing error")  
     
def parse_vt_file(inf, outf):
    ih = open(inf)
    oh = open(outf, "w+")

    for line in ih:
        write_record(oh, line.strip())
    oh.close()

def extract_url_feed_tar(fi, outf, istar = True):
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
            write_record(fd, line.strip())
    tar.close()
    fd.close()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print ("Usage: {} date <startdate> <enddate>".format(sys.argv[0]))
        print ("Usage: {} file <vtfile> <outfile>".format(sys.argv[0]))
        exit()
    option = sys.argv[1]
    if option == "date": 
        parse_vt_files(sys.argv[2], sys.argv[3])
    elif option == "file":
        parse_vt_file(sys.argv[2], sys.argv[3])
