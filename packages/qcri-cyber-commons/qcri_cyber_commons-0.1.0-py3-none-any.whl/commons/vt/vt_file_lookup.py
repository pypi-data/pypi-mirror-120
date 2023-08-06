'''
Gather VT File data
'''
import vt_private as vtp
import sys
import json
from urllib.parse import urlparse
import time

SPEED = 0.1
def vt_file_file(hash_file, outfile, relation, keyindex):
    of = open(outfile, "w+")
    with open(hash_file) as df:
        for hashf in df:
            time.sleep(SPEED)
            hashf = hashf.strip()
            of.write("{}\n".format(json.dumps(vtp.getFile(hashf, relation, keyindex))))
    of.close()

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: {} <hash-file> <output-file> <relationship> <keyindex>".format(sys.argv[0]))
        exit()
    hashfile = sys.argv[1]
    outputfile = sys.argv[2]
    #contacted_domains
    relation = sys.argv[3]
    keyindex = int(sys.argv[4])

    vt_file_file(hashfile, outputfile, relation, keyindex)
