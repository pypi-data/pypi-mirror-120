import glob
import json
import pandas as pd

def update_labels(fn, labels):
    df1 = pd.read_csv(fn, header = None)
    df1.columns = ['label']
    current_labels = set(df1['label'].unique())
    all_labels = current_labels | set(labels)
    df = pd.DataFrame(all_labels)
    df.to_csv(fn, header = False, index = False)
    return all_labels

all_attacks = update_labels("/export/sec02/nabeel/Common/utils/vt_attack_universe.txt", [])

def vt_json_to_dict(line, attacks):
    record = dict()
    try:
        jobj = json.loads(line)
        url = jobj["url"].strip("/")
        record["url"] = url
        record["scan_date"] = jobj["scan_date"]
        record["positives"] = jobj["positives"]
        record["first_seen"] = jobj["first_seen"]
        record["last_seen"] = jobj["last_seen"]
        
        #additional information
        record["ip"] = "NONE"
        try:
            record["ip"] = jobj["additional_info"]["resolution"]
        except KeyError as e:
            pass
        record["content_hash"] = "NONE"
        try:
            record["content_hash"] = jobj["additional_info"]["Response content SHA-256"]
        except KeyError as e:
            pass
        record["rlength"] = -1
        try:
            record["rlength"] = jobj["additional_info"]["rlength"]
        except KeyError as e:
            pass
        
        record["url_after_redirects"] = "NONE"
        try:
            record["url_after_redirects"] = jobj["additional_info"]["URL after redirects"]
        except KeyError as e:
            pass
        
        for attack in attacks:
            record[attack] = 0
        
        scans = jobj["scans"]
        record["avs"] = ""
        for key, value in scans.items():
            try:
                #we keep track of only those attack types we identified
                #ignore those not on the list through this exception block
                record[value['result']] += 1
            except KeyError as e:
                pass
            if value["detected"] == True:
                if len(record["avs"]) > 0:
                    record["avs"] += '#'
                record["avs"] += key + ':' + value['result']
    except KeyError as e:
        #print(e)
        pass
    return record

#consider multiple files matching a regular expression
def vt2df(filepath, attacks):
    records = []
    for filename in glob.iglob(filepath):
        fp = open(filename, encoding = 'utf-8')
        for line in fp:
            if len(line.strip()) == 0:
                continue
            records.append(vt_json_to_dict(line.strip(), attacks))
    return pd.DataFrame(records)

#consider only one file
def vt2df_file(filename, attacks):
    records = []
    fp = open(filename, encoding = 'utf-8')
    for line in fp:
        if len(line.strip()) == 0:
            continue
        records.append(vt_json_to_dict(line.strip(), attacks))
    return pd.DataFrame(records)
