#!/usr/bin/python
'''
Author: @nabeelxy
Description:
This file is specifically prepared for phicious project
Given a list of domains in a file, it produces a file with the following features:
'''

import sys
import pdns
from datetime import datetime
import tldextract

def get_2ld(fqdn):
    ext = tldextract.extract(fqdn)
    return ext.domain + "." + ext.suffix

def get_ip_features(ip, firstseen_before = None):
    first_seen = None
    last_seen = None
    count = 0
    domain_set = set()
    first_seen_date = None
    last_seen_date = None
    LAST_SEEN_AFTER = "20200601 00:00"
    mappings = pdns.pdns_ip(ip, firstseen_before, None, None, LAST_SEEN_AFTER, 5000)

    if mappings == None:
        return None
    
    for entry in mappings:
        if first_seen == None:
            first_seen = entry["time_first"]
        elif first_seen > entry["time_first"]:
            first_seen = entry["time_first"]
        if last_seen == None:
            last_seen = entry["time_last"]
        elif last_seen < entry["time_last"]:
            last_seen = entry["time_last"]
        domain_set.add(get_2ld(entry["rrname"]))
        count += entry["count"]
    #firstseen, lastseen, query count, #apex_domains
    return [first_seen, last_seen, count, len(domain_set)]

def get_features_file(domain_file, outfile, firstseen_before = None):
    df = open(domain_file, encoding = 'utf-8')
    of = open(outfile, "w+", encoding = 'utf-8')
    for ip in df:
        ip = ip.strip()
        out = get_ip_features(ip, firstseen_before)
        if out != None:
            first_seen_date = None
            last_seen_date = None
            if out[0] != None:
                first_seen_date = datetime.fromtimestamp(out[0])
            if out[1] != None:
                last_seen_date = datetime.fromtimestamp(out[1])
            of.write("{},{},{},{},{}\n".format(ip, first_seen_date, last_seen_date, out[2], out[3]))
    of.close()  
    df.close() 

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: python {} input_domain_file output_file firstseen_before(YYYYMMDD HH:MM)".format(sys.argv[0]))
        exit()
        
    domainf = sys.argv[1] #input domain  file
    outf = sys.argv[2] #output file
    firstseen_before = sys.argv[3]
    if firstseen_before.lower() == "none":
        firstseen_before = None
    get_features_file(domainf, outf, firstseen_before)
