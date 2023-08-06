import hashlib
import os
import re

import pandas as pd

from commons.utils.maxmind_tools import MyASN

#### global variables############################################################
# Load brands considered
# TODO: make global variables local and load them in main program
brands_df = pd.read_csv("../data/pt_alexa_brands_20210108.csv", header=None)
brands_df.columns = ["brand", "domain", "description"]
brands = set(brands_df["brand"].unique())

parking_df = pd.read_csv("../data/park_ns.txt", header=None, sep=" ")
parking_df.columns = ["name", "ns", "domain"]
parking = set(parking_df["domain"].unique())

asn = MyASN("/export/sec03/asn/GeoIPASN_each_day/geo_20210430_GeoIPASNum.dat")

####################################################################################
# utils
import pickle


# save data structure to a file
def save_ds(ds, filename):
    pickle.dump(ds, open(filename, 'wb'))


# load the data structure from file
def load_ds(filename):
    return pickle.load(open(filename, 'rb'))


def line_prepender(filename, line):
    if not os.path.exists(filename):
        open(filename, "w").close()

    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)


def read_first_line(filename):
    first_line = None
    if os.path.exists(filename):
        with open(filename) as f:
            first_line = f.readline().strip()
    return first_line


def get_sha256_hex(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()


def contains_ip(st):
    if re.match('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', st) != None:
        return True
    return False
