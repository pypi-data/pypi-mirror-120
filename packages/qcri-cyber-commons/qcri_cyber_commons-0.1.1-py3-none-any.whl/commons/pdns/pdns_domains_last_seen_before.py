#!/usr/bin/python
'''
Author: @nabeelxy
Description:
This file is specifically prepared for phicious project
Given a list of domains in a file, it produces a file with the following features:
'''

import sys
import pdns
import tldextract

def get_2ld(fqdn):
    ext = tldextract.extract(fqdn)
    return ext.domain + "." + ext.suffix

def get_pdns_features(domain, firstseen_before = None):
    first_seen = None
    last_seen = None
    count = 0
    ip_set = set()
    first_seen_date = None
    last_seen_date = None
    LAST_SEEN_AFTER = "20150601 00:00"
    mappings = pdns.pdns_domain(domain, firstseen_before, None, None, LAST_SEEN_AFTER, 5000)

    if mappings == None:
        return None
    
    for entry in mappings:
        for ip in entry["rdata"]:
            ip_set.add(ip)
    return ip_set

def get_features_file(domain_file, outfile, firstseen_before = None):
    df = open(domain_file)
    of = open(outfile, "w+")
    for domain in df:
        domain = domain.strip()
        ip_set = get_pdns_features(domain, firstseen_before)
        if ip_set != None:
            for ip in ip_set:
                of.write("{} {}\n".format(domain, ip))
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
