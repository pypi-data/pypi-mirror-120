'''
Gather VT IP data
'''
import vt_private as vtp
import sys
import json
from urllib.parse import urlparse
import time

SPEED = 0.1
def cert_file(ip_file, outfile, relation, keyindex):
    of = open(outfile, "w+")
    with open(ip_file) as df:
        for ip in df:
            time.sleep(SPEED)
            ip = ip.strip()
            of.write("{}\n".format(json.dumps(vtp.getIP(ip, relation, keyindex))))
    of.close()

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: {} <ip-file> <output-file> <relationship> <keyindex>".format(sys.argv[0]))
        exit()
    ipfile = sys.argv[1]
    outputfile = sys.argv[2]
    #historical_ssl_certificates,historical_whois, resolutions
    relation = sys.argv[3]
    keyindex = int(sys.argv[4])

    cert_file(ipfile, outputfile, relation, keyindex)
