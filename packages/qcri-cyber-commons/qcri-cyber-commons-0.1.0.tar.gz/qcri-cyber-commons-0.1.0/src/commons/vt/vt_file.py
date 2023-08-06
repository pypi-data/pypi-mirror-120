import vt_private as vtp
import sys
import json
from urllib.parse import urlparse
import time

SPEED = 0.1

def scan_file(domain_file, outfile, keyindex):
    of = open(outfile, "w+")
    with open(domain_file, encoding = 'utf-8') as df:
        for line in df:
            time.sleep(SPEED)
            line = line.strip()
            if line.startswith("http"):
                domain = line
            else: #if the protocol is not specified, use https
                domain = "https://" + line
            of.write("{}\n".format(json.dumps(vtp.scan(domain, keyindex))))
    of.close()

def report_file(scanid_file, outfile, keyindex):
    of = open(outfile, "w+")
    with open(scanid_file) as sf:
        for str in sf:
            json_obj = json.loads(str)
            try:
                time.sleep(SPEED)
                of.write("{}\n".format(json.dumps(vtp.getReport(json_obj['scan_id'], keyindex))))
            except KeyError as e:
                pass
    of.close()

def process_vt_results(results_file, outfile):
    of = open(outfile, "w+")
    with open(results_file) as rf:
        for str in rf:
            #str = str.replace('\'', '"').replace("True", "\"True\"").replace("False", "\"False\"")
            #print(str)
            json_obj = json.loads(str)
            of.write("{} {}\n".format(urlparse(json_obj['url']).netloc, json_obj['positives']))
    of.close()

domainfile = sys.argv[1]
outputfile = sys.argv[2]
keyindex = int(sys.argv[3])
scan_file(domainfile, outputfile, keyindex)
#time.sleep(300)
report_file(outputfile, outputfile + ".report", keyindex)
