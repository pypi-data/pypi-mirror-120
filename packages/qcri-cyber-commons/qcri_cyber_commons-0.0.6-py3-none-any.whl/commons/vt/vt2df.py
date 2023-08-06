'''
Description: Parsing VT reports
Author: nabeelxy
'''
import pandas as pd
import json
from datetime import datetime, timedelta
import sys
import glob
import tarfile

BASE_VT_DIR = "/export/sec03/vt/vt_url_feed"

def load_data(in_file):
    df = pd.read_csv(in_file, header = None)
    df.columns = ['name']
    return set(df['name'].unique())

def update_data(in_file, new_data):
    all_data = new_data
    try:
        df = pd.read_csv(in_file, header = None)
        df.columns = ['name']
        all_data = set(df['name'].unique()) | new_data
    except: #if the file is empty or non-existent
        pass
    pd.DataFrame(all_data).to_csv(in_file, header = False, index = False)

#From all VT reports find out all attack types and engine names
#rf - file handle
def get_attacks_engines(rf):
    attacks = set()
    engines = set()
    
    for line in rf:
        try:
            jobj = json.loads(line.strip())
            scans = jobj["scans"]
            for key, value in scans.items():
                engines.add(key)
                attacks.add(value['result'])

        except KeyError as e:
            pass
    rf.seek(0)

    return attacks, engines

def vt2df(rf, attacks = None, engine_names = None, only_pos = True, attack_labels = False):

    # if attacks and engien names are not specified, first get the sets
    if attacks == None and engine_names == None:
        attacks, engine_names = get_attacks_engines(rf)

    df = pd.DataFrame()
    
    records = list()
    
    for line in rf:
        try:
            jobj = json.loads(line.strip())
            record = dict()
            record["positives"] = jobj["positives"]
            if only_pos and record["positives"] == 0:
                continue
            url = jobj["url"].strip("/")
            record["url"] = url
            record["scan_date"] = jobj["scan_date"]
            record["scan_id"] = jobj["scan_id"]
            record["total"] = jobj["total"]
            record["first_seen"] = jobj["first_seen"]
            record["last_seen"] = jobj["last_seen"]

            #additional information
            record["sophos category"] = None
            try:
                record["sophos category"] = jobj["additional_info"]["sophos category"]
            except:
                pass
            record["Webroot category"] = None
            try:
                record["Webroot category"] = jobj["additional_info"]["Webroot category"]
            except:
                pass
            record["x-xss-protection"] = None
            try:
                record["x-xss-protection"] = jobj["additional_info"]["Response headers"]["x-xss-protection"]
            except:
                pass
            record["x-frame-options"] = None
            try:
                record["x-frame-options"] = jobj["additional_info"]["Response headers"]["x-frame-options"]
            except:
                pass
            record["set-cookie"] = None
            try:
                record["set-cookie"] = jobj["additional_info"]["Response headers"]["set-cookie"]
            except:
                pass
            record["Response content SHA-256"] = None
            try:
                record["Response content SHA-256"] = jobj["additional_info"]["Response content SHA-256"]
            except:
                pass
            record["Response code"] = None
            try:
                record["Response code"] = jobj["additional_info"]["Response code"]
            except:
                pass
            record["Forcepoint ThreatSeeker category"] = None
            try:
                record["Forcepoint ThreatSeeker category"] = jobj["additional_info"]["Forcepoint ThreatSeeker category"]
            except:
                pass

            record["Comodo Valkyrie Verdict category"] = None
            try:
                record["Comodo Valkyrie Verdict category"] = jobj["additional_info"]["Comodo Valkyrie Verdict category"]
            except:
                pass


            record["ip"] = None
            try:
                record["ip"] = jobj["additional_info"]["resolution"]
            except:
                pass
            record["content_hash"] = None
            try:
                record["content_hash"] = jobj["additional_info"]["Response content SHA-256"]
            except:
                pass
            record["rlength"] = None
            try:
                record["rlength"] = jobj["additional_info"]["rlength"]
            except:
                pass
            record["url_after_redirects"] = None
            try:
                record["url_after_redirects"] = jobj["additional_info"]["URL after redirects"]
            except:
                pass

            for attack in attacks:
                record[attack] = 0
            for engine in engine_names:
                record[engine] = 1 
       
            #1 - not present
            #2 - unrated site
            #3 - marked benign
            #4 - marked malicious 
            scans = jobj["scans"]
            if attack_labels == True: #mark with attack label
                for key, value in scans.items():
                    record[value['result']] += 1
                    record[key] = value['result']
            else: #use the above code for detected/undtected sites
                for key, value in scans.items():
                    record[value['result']] += 1
                    if value['detected']:
                        record[key] = 4 #marked malicious
                    elif value['result'] == "unrated site":
                        record[key] = 2
                    else:
                        record[key] = 3 #marked bengin
                
                    
            records.append(record)
        except KeyError as e:
            print(e)
            pass
    return pd.DataFrame(records)


def vt_parse_attacks_engines_dir(startdate, enddate, basedir = BASE_VT_DIR):
    s_date = datetime.strptime(startdate.strip(), "%Y%m%d").date()
    e_date = datetime.strptime(enddate.strip(), "%Y%m%d").date()
    delta = e_date - s_date
    files = []
    for i in range(delta.days + 1):
        curr_date = s_date + timedelta(i)
        files += glob.glob("{}/url-feed-{}T*.tar.bz2".format(basedir, curr_date.strftime("%Y%m%d")))
    
    return vt_parse_attacks_engines(files)

#find the unique attacks and engines mentioned in the report
#VT report engines change over time - hence we need to reprofile
def vt_parse_attacks_engines(files):
    master_attacks = set()
    master_engines = set()
    for fi in files:
        try:
            if fi.endswith(".bz2"):
                tar = tarfile.open(fi, "r:bz2")
                for item in tar:
                    fh = tar.extractfile(item)
                    attacks, engines = get_attacks_engines(fh)
                    master_attacks |= attacks
                    master_engines |= engines
            else: # uncompressed files
                fh = open(fi)
                attacks, engines = get_attacks_engines(fh)
                master_attacks |= attacks
                master_engines |= engines
        except Exception as e:
            print(e)
            pass
            print("ERROR: parsing file {}".format(fi))

    return master_attacks, master_engines

def vt_parse_data_dir(startdate, enddate, attacks, engines, only_pos = True, basedir = BASE_VT_DIR, attack_labels = False):
    s_date = datetime.strptime(startdate.strip(), "%Y%m%d").date()
    e_date = datetime.strptime(enddate.strip(), "%Y%m%d").date()
    delta = e_date - s_date
    files = []
    for i in range(delta.days + 1):
        curr_date = s_date + timedelta(i)
    files += glob.glob("{}/url-feed-{}T*.tar.bz2".format(basedir, curr_date.strftime("%Y%m%d")))
    return vt_parse_data(startdate, enddate, attacks, engines, only_pos, files, attack_labels)

def vt_parse_data_files(attacks, engines, only_pos, files, attack_labels):
    if attacks == None and engines == None:
        attacks, engines = vt_parse_attacks_engines(startdate, enddate)

    dfs = list()
    df = None
    for fi in files:
        try:
            if fi.endswith(".bz2"):
                tar = tarfile.open(fi, "r:bz2")
                for item in tar:
                    fh = tar.extractfile(item)
                    df = vt2df(fh, attacks, engines, only_pos, attack_labels)
                    #de-dup records
                    #current policy - keep the record with the highest positive (we may change this later)
                    df = df.sort_values(by = "positives", ascending = False)
                    df = df.drop_duplicates(subset = ["url"], keep = "first")
                    dfs.append(df)
            else: #regular file
                fh = open(fi)
                df = vt2df(fh, attacks, engines, only_pos, attack_labels)
                #de-dup records
                #current policy - keep the record with the highest positive (we may change this later)
                df = df.sort_values(by = "positives", ascending = False)
                df = df.drop_duplicates(subset = ["url"], keep = "first")
                dfs.append(df)
        except Exception as e:
            print(e)
            pass
            print("ERROR: parsing file {}".format(fi))
    if len(dfs) > 0:
        df = pd.concat(dfs)
        df = df.sort_values(by = "positives", ascending = False)
        df = df.drop_duplicates(subset = ["url"], keep = "first")

    return df


if __name__ == "__main__":
    option = sys.argv[1] #engines|engines_file|parse|parse_file

    if option == "engines": #parse a set of files in a folder that are annotated with date
        startdate = sys.argv[2] #YYYYMMDD
        enddate = sys.argv[3] #YYYYMMDD
        basedir = sys.argv[4]
        attacks, engines = vt_parse_attacks_engines_dir(startdate, enddate, basedir)
        update_data("attacks.csv", attacks)
        update_data("engines.csv", engines)
    elif option == "engines_file":
        infile = sys.argv[2] #input file
        attacks, engines = vt_parse_attacks_engines([infile])
        update_data("attacks.csv", attacks)
        update_data("engines.csv", engines)
    elif option == "parse": #parse a set of files in a folder that are annotated with date
        startdate = sys.argv[2] #YYYYMMDD
        enddate = sys.argv[3] #YYYYMMDD
        basedir = sys.argv[4]
        outfile = sys.argv[5] #file where we are going to save the parsed data
        labels = int(sys.argv[5]) # 1 for true, 0 for false
        attacks = load_data("attacks.csv")
        engines = load_data("engines.csv")
        df = vt_parse_data_dir(startdate, enddate, attacks, engines, True, basedir, labels)
        df.to_csv(outfile, header = True, index = False)
    elif option == "parse_file": #parse a single file
        infile = sys.argv[2]
        outfile = sys.argv[3]
        labels = int(sys.argv[4]) # 1 for true, 0 for false
        attacks = load_data("attacks.csv")
        engines = load_data("engines.csv")
        df = vt_parse_data_files(attacks, engines, False, [infile], labels)
        df.to_csv(outfile, header = True, index = False)
    else:
        print("Unrecognized engine")
