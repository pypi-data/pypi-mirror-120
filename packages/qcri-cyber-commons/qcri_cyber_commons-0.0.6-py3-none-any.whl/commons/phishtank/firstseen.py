"""
Get the firstseen records from phishtank and analyze
"""
import copy
import sys
from datetime import datetime

import pandas as pd
import psycopg2

from commons.utils.domain_tools import get_2ld, get_fqdn, load_pub_types, get_pub_type, get_protocol

# table schema
# create table phishtank (url text primary key, domain varchar(500), phish_detail_url varchar(1000), first_submitted timestamp, last_submitted timestamp, no_submissions integer, first_verified tiimestamp, last_verified timestamp, verified text, online text, target text);

databasename = "phishing"
tablename = "phishtank"


def db_conn():
    conn = None
    try:
        conn = psycopg2.connect(database=databasename, user="postgres", password="postgres", port=5432)
    except:
        pass
    return conn


def db_close(conn):
    conn.close()


def get_firstseen(timestamp_file):
    conn = db_conn()
    urls = []
    if conn == None:
        print("Unable to connect to the DB")
        return urls

    cursor = conn.cursor()
    ts_str = open(timestamp_file).read().strip()
    ts_dt = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
    query = "SELECT url, first_submitted FROM {} WHERE first_submitted > %s".format(tablename)
    params = (ts_str,)
    cursor.execute(query, params)
    rs = cursor.fetchall()
    first_submitted = ts_dt
    if rs != None:
        for record in rs:
            if first_submitted < record[1]:
                first_submitted = record[1]
            urls.append(record[0])
    fh = open(timestamp_file, "w")
    fh.write("{}".format(first_submitted.strftime("%Y-%m-%d %H:%M:%S")))
    fh.close()
    cursor.close()
    db_close(conn)
    return urls


def enumerate_urls(urls):
    pubs = load_pub_types()
    urls = set([url.strip('"/') for url in urls])
    new_urls = copy.deepcopy(urls)
    for url in urls:
        protocol = get_protocol(url)
        fqdn = get_fqdn(url)
        apex = get_2ld(fqdn)
        urlprime = url
        if protocol == "https":
            urlprime = urlprime.replace("https", "http", 1)
        elif protocol == "http":
            urlprime = urlprime.replace("http", "https", 1)
        # if it a protocol other than http/https, ignore
        if urlprime != url:
            new_urls.add(urlprime)

        # if protocol is not specified, use https as attackers
        # are increasingly forced to use https to avoid suspision
        if protocol == None:
            protocol = "https"

        if fqdn != None:
            fqdn = protocol + "://" + fqdn
            new_urls.add(fqdn)

        # only add non-public apex domains
        if apex != None:
            pub_type = get_pub_type(apex, pubs)
            if pub_type == "NotFound":
                apex = protocol + "://" + apex
                new_urls.add(apex)
    return new_urls


def save_urls(filename, urls):
    df = pd.DataFrame(urls)
    df.to_csv(filename, header=False, index=False, sep=" ")


if __name__ == "__main__":
    conn = db_conn()
    urls = get_firstseen(sys.argv[1])
    new_urls = enumerate_urls(urls)
    save_urls(sys.argv[2], new_urls)
