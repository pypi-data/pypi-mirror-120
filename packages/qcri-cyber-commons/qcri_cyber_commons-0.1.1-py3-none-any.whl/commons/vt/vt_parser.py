import json
import sys
from urllib.parse import urlparse

import pandas as pd


def get_fqdn(url):
    try:
        uri = urlparse(url)
        if uri:
            return uri.netloc
    except Exception as e:
        pass
    return None


def parse_domain_cert(vtfile, outfile):
    of = open(outfile, "w+")
    with open(vtfile) as sf:
        for str in sf:
            json_obj = json.loads(str)
            try:
                for cert in json_obj["data"]:
                    subject = cert["attributes"]["subject"]["CN"].strip()
                    issuer = cert["attributes"]["issuer"]["O"].strip()
                    start = cert["attributes"]["validity"]["not_before"].strip()
                    end = cert["attributes"]["validity"]["not_after"].strip()
                    san = cert["attributes"]["extensions"]["subject_alternative_name"]
                    of.write("{}##{}##{}##{}##{}\n".format(subject, start, end, issuer, san))
            except KeyError as e:
                # print(e)
                pass
    of.close()


def parse_domain_whois(vtfile, outfile):
    records = []
    with open(vtfile) as vf:
        for line in vf:
            json_obj = json.loads(line.strip())
            try:
                for whois in json_obj["data"]:
                    registrant = None
                    registrar = None
                    whoisserver = None
                    creation = None
                    update = None
                    expiration = None
                    ns = None
                    domain = whois["attributes"]["whois_map"]["Domain Name"].lower()
                    try:
                        registrant = whois["attributes"]["registrant_name"].lower()
                    except:
                        registrant = None
                        pass
                    try:
                        registrar = whois["attributes"]["whois_map"]["Registrar"].lower()
                    except:
                        try:
                            registrar = whois["attributes"]["registrar_name"].lower()
                        except:
                            regisrar = None
                    try:
                        creation = whois["attributes"]["whois_map"]["Creation Date"]
                    except:
                        creation = None

                    try:
                        expiration = whois["attributes"]["whois_map"]["Registry Expiry Date"]
                    except:
                        expiration = None

                    try:
                        update = whois["attributes"]["whois_map"]["Updated Date"]
                    except:
                        update = None

                    try:
                        ns = whois["attributes"]["whois_map"]["Name Server"]
                    except:
                        ns = None

                    try:
                        whoiserver = whois["attributes"]["whois_map"]["Registrar WHOIS Server"]
                    except:
                        whoisserver = None

                    # print("registrant country = {}".format(whois["attributes"]["whois_map"]["Registrant Country"]))
                    records.append([domain, registrant, registrar, whoisserver, creation, expiration, ns, update])
            except KeyError as e:
                print(e)
                pass
    df = pd.DataFrame().from_records(records)
    df.to_csv(outfile, index=False, header=False)


def parse_ip_whois(vtfile, outfile):
    of = open(outfile, "w")
    with open(vtfile) as vf:
        for line in sf:
            json_obj = json.loads(line.strip())
            try:
                for whois in json_obj["data"]:
                    print(whois)
            except KeyError as e:
                print(e)
                pass


# before create the dataframe, we need to the attack types and engine names
def get_attacks_engines(rfile):
    rf = open(rfile)
    engines = set()
    attacks = set()
    for line in rf:
        try:
            jobj = json.loads(line.strip())
            scans = jobj["scans"]
            for key, value in scans.items():
                engines.add(key)
                attacks.add(value['result'])
        except KeyError as e:
            pass
    return [attacks, engines]


def parse_domain_reports(rfile, ofile):
    rf = open(rfile)
    [attacks, engine_names] = get_attacks_engines(rfile)
    records = list()

    for line in rf:
        try:
            jobj = json.loads(line.strip())
            url = jobj["url"].strip("/")
            record = dict()
            record["url"] = url
            record["scan_date"] = jobj["scan_date"]
            record["positives"] = jobj["positives"]

            for attack in attacks:
                record[attack] = 0
            for engine in engine_names:
                record[engine] = -2

            scans = jobj["scans"]
            for key, value in scans.items():
                record[value['result']] += 1
                if value['detected']:
                    record[key] = 1
                else:
                    record[key] = 0

                if value['result'] == "unrated site":
                    record[key] = -1

            records.append(record)
        except KeyError as e:
            print(e)
            pass
    df = pd.DataFrame(records)
    df['fqdn'] = df['url'].apply(lambda x: get_fqdn(x) if x != None else x)
    df.to_csv(ofile, header=True, index=False)


def parse_ip_resolutions(rfile, ofile):
    rf = open(rfile)
    records = list()

    for line in rf:
        try:
            jobj = json.loads(line.strip())
            data = jobj["data"]
            for rec in data:
                tmp = []
                attr = rec["attributes"]
                tmp.append(attr["host_name"])
                tmp.append(attr["ip_address"])
                tmp.append(attr["date"])
                records.append(tmp)
        except KeyError as e:
            print(e)
            pass
    df = pd.DataFrame().from_records(records)
    df.to_csv(ofile, header=False, index=False, sep=" ")


if __name__ == "__main__":
    option = sys.argv[1]
    infile = sys.argv[2]
    outfile = sys.argv[3]
    if option == "domain_whois":
        parse_domain_whois(infile, outfile)
    elif option == "domain_report":
        parse_domain_reports(infile, outfile)
    elif option == "ip_resolution":
        parse_ip_resolutions(infile, outfile)
    elif option == "domain_cert":
        parse_domain_cert(infile, outfile)
