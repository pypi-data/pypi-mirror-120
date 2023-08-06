'''
Description: newly observed domains. Create a dictionary in memory. Summerize
the data for the data range specified
Author: @nabeelxy 
Usage: python cert2dom.py YYYYMMDD YYYYMMDD
'''

import ast
import os
import sys
from datetime import timedelta

import pandas as pd

from commons.utils.date_tools import dt2str, ts2dt
from commons.utils.domain_tools import get_2ld

BASE_CT = "/export/sec04/phishing/data"


def get_domains(startdate, enddate, isapex=False):
    s_date = ts2dt(startdate.strip(), "%Y%m%d")
    e_date = ts2dt(enddate.strip(), "%Y%m%d")

    delta = e_date - s_date
    domains = dict()
    count = 0
    for i in range(delta.days + 1):
        curr_date = s_date + timedelta(i)
        name = "certs_" + dt2str(curr_date, "%Y%m%d") + ".log"
        certs = open(os.path.join(BASE_CT, name), "r")
        for cert in certs:
            cert = ast.literal_eval(cert.strip())
            seen = int(cert['data']['seen'])
            for domain in cert['data']['leaf_cert']['all_domains']:
                count += 1
                if domain.startswith("*."):
                    domain = domain[2:]
                domain = domain.strip()
                if domain == "" or len(domain) == 0:
                    continue

            if isapex:
                try:
                    domain = get_2ld(domain)
                except:
                    print("Unable to get 2ld: {}".format(domain))
                    pass
                    continue

            if domain in domains:
                if seen < domains[domain][0]:
                    domains[domain][0] = seen
                if seen > domains[domain][1]:
                    domains[domain][1] = seen
                domains[domain][2] += 1
            else:
                # firstseen, lastseen, count
                domains[domain] = [seen, seen, 1]
    # print("all = {}".format(count))
    # print("processed = {}".format(len(domains)))
    return domains


def save2file(filename, domains):
    df = pd.DataFrame(domains.items())
    df.to_csv(filename, index=False, header=False)


if __name__ == "__main__":
    startd = sys.argv[1]  # YYYYMMDD
    endd = sys.argv[2]  # YYYYMMDD
    outf = sys.argv[3]
    save2file(outf, get_domains(startd, endd))
