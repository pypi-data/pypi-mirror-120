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
import csv
import pandas as pd

def get_2ld(fqdn):
    ext = tldextract.extract(fqdn)
    return ext.domain + "." + ext.suffix

#domain - domain name
#firstseen_before - None or any specific date
#num_ips - number of latest IPs to collect (some domains have thousands of IPs. So, limiting the collection
#useful. Old IPs anyway do not contribute much.
def get_pdns_features(domain, firstseen_before = None, num_ips = None):
    first_seen = None
    last_seen = None
    count = 0
    ip_set = set()
    first_seen_date = None
    last_seen_date = None
    LAST_SEEN_AFTER = "20150101 00:00"
    mappings = pdns.pdns_domain(domain, firstseen_before, None, None, LAST_SEEN_AFTER, 5000)
    mappings_ns = pdns.pdns_domain(get_2ld(domain), firstseen_before, None, None, LAST_SEEN_AFTER, 100, "NS")
    mappings_soa = pdns.pdns_domain(get_2ld(domain), firstseen_before, None, None, LAST_SEEN_AFTER, 100, "SOA")
    ns_set = set()
    soa_set = set()
    ns_domain = None #idicates if the ns domain is same as the apex domain under consideration
    soa_domain = None
    current_ip = None
    latest_ips = list()

    if mappings == None:
        return None
    
    if mappings_ns != None:
        for entry_ns in mappings_ns:
            for domain in entry_ns["rdata"]:
                domain = domain.strip(".") #remove ending dot, if any
                ns_set.add(get_2ld(domain))
        if get_2ld(domain) in ns_set:
            ns_domain = True

    if mappings_soa != None:
        for entry_soa in mappings_soa:
            for record in entry_soa["rdata"]:
                items = record.split()
                if len(items) > 2:
                    admin_domain = items[1].strip(".") #remove ending dot, if any
                    soa_set.add(get_2ld(admin_domain))
        if get_2ld(domain) in soa_set:
            soa_domain = True

    for entry in mappings:
        if first_seen == None:
            first_seen = entry["time_first"]
        elif first_seen > entry["time_first"]:
            first_seen = entry["time_first"]
        if last_seen == None:
            last_seen = entry["time_last"]
        elif last_seen < entry["time_last"]:
            last_seen = entry["time_last"]
        for ip in entry["rdata"]:
            if current_ip == None:
                current_ip = ip
            ip_set.add(ip)
            #maintain the ordered list (if number of ips to collect is specified)
            if num_ips != None and ip not in latest_ips and len(latest_ips) < num_ips:
                latest_ips.append(ip)
        count += entry["count"]

    #firstseen, lastseen, query count, #name servers, ns domain, #soa domains, soa_domain, current ip, all ips, all NSes, latest IPs
    return [first_seen, last_seen, count, len(ip_set), len(ns_set), ns_domain, len(soa_set), soa_domain, ip, ip_set, ns_set, latest_ips]

def get_features_file(domain_file, outfile, firstseen_before = None, num_ips = 20):
    df = open(domain_file, encoding = 'utf-8')
    of = open(outfile, "w+", encoding = 'utf-8')
    for domain in df:
        domain = domain.encode("idna").decode().strip()
        out = get_pdns_features(domain, firstseen_before, num_ips)
        duration = -1
        if out != None:
            first_seen_date = None
            last_seen_date = None
            if out[0] != None:
                first_seen_date = datetime.fromtimestamp(out[0])
            if out[1] != None:
                last_seen_date = datetime.fromtimestamp(out[1])
            if out[0] != None and out[1] != None:
                duration = (out[1] - out[0])/86400 # number of days
            of.write("{},{},{},{},{},{},{},{},{},{},{},\"{}\",\"{}\"\n".format(domain, first_seen_date, last_seen_date, out[2], out[3], out[4], out[5], out[6], out[7],
                                                              duration, out[8], out[10], out[11]))
    of.close()  
    df.close() 

def pdnscsv2df(csvfile):
    records = []
    with open(csvfile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            records.append(row)
    
    df_pdns = pd.DataFrame().from_records(records)
    df_pdns.columns = ["domain",
                   "firstseen", 
                   "lastseen", 
                   "query count", 
                   "#ips",
                   "#name servers", 
                   "ns domain", 
                   "#soa domains", 
                   "soa_domain", 
                   "duration", 
                   "current ip", 
                   "all NSes", 
                   "latest IPs"]
    return df_pdns

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
