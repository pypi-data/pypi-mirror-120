import vt_query_host as vtq
import sys
import tldextract
import entropy
from datetime import datetime

def get_set(filename):
    words = set()
    fn = open(filename)
    for word in fn:
        words.add(word.strip())
    return words

def fs_ls(infilename, outfilename):
    infile = open(infilename)
    outfile = open(outfilename, "w+")

    for domain in infile:
        domain = domain.strip()
        record = vtq.get_record(domain, "vt_nod")
        if record == None:
            continue
        outfile.write("{}##{}##{}##{}##{}\n".format(domain, record[0], 
                     record[1], datetime.fromtimestamp(record[0]).strftime('%Y-%m-%d %H:%M:%S'),
                     datetime.fromtimestamp(record[1]).strftime('%Y-%m-%d %H:%M:%S'))) 
    outfile.close()

def subdomains(infilename, outfilename, threshold):
    infile = open(infilename)
    outfile = open(outfilename, "w+")

    sub_freq = dict()
    for domain in infile:
        domain = domain.strip()
        record = vtq.get_record(domain, "vt_nod")
        if record == None:
            continue
        fqdns = record[4].split('##')
        for fqdn in fqdns:
            ext = tldextract.extract(fqdn)
            if ext.subdomain == None or len(ext.subdomain) == 0:
                continue
            if '.' in ext.subdomain:
                continue
            if ext.subdomain not in sub_freq:
                sub_freq[ext.subdomain] = 0
            sub_freq[ext.subdomain] += 1
    print(sub_freq)
    for subdom, freq in sub_freq.items():
        if freq > threshold:
            outfile.write("{} {}\n".format(subdom, freq))
    outfile.close()

if __name__ == "__main__":
    method = sys.argv[1] #extract,subdoms
    if method == "extract":
        fs_ls(sys.argv[2], sys.argv[3])
    elif method == "subdoms":
        subdomains(sys.argv[2], sys.argv[3], int(sys.argv[4]))
