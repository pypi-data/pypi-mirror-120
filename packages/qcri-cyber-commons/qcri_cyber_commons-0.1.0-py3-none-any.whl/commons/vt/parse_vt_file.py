import tarfile
import json
import glob
import sys
import os
import time
from urllib.parse import urlparse
from datetime import date, timedelta, datetime


def extract_vt(fi, outf):
    fd = open(outf, "w+")
    file_obj = open(fi)	

    for line in file_obj:
        try:
            url_obj = json.loads(line)
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
        except:
            pass
            continue
    file_obj.close()
    fd.close()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print ("Usage: {} <vt_report_file> <output file>".format(sys.argv[0]))
        exit()
    extract_vt(sys.argv[1], sys.argv[2])
