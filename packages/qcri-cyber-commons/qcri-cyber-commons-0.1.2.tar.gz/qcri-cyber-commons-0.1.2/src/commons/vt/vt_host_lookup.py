'''
Collect VT Host related data
'''
import vt_private as vtp
import sys
import json
from urllib.parse import urlparse
import time
import tldextract 

SPEED = 0.1
def get_2ld(fqdn, only_tld = False):
    try:
        ext = tldextract.extract(fqdn)
        if len(ext.domain) == 0 or len(ext.suffix) == 0:
            return None
        else:
            if only_tld:
                return ext.suffix
            else:
                return ext.domain + "." + ext.suffix
    except Exception as e:
        print("ERROR - something wrong with the FQDN: {}".format(fqdn))
        print(e)
        pass
    return None

def dcert_file(domain_file, outfile, relation, keyindex):
    of = open(outfile, "w+")
    with open(domain_file) as df:
        for line in df:
            time.sleep(SPEED)
            of.write("{}\n".format(json.dumps(vtp.getDomain(line.strip(), relation, keyindex))))
    of.close()

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: {} <domain-file> <output-file> <relationship> <keyindex>".format(sys.argv[0]))
        exit()

    domainfile = sys.argv[1]
    outputfile = sys.argv[2]
    #resolutions,siblings,subdomains,referrer_files 
    relation = sys.argv[3]
    keyindex = int(sys.argv[4])
    dcert_file(domainfile, outputfile, relation, keyindex)
