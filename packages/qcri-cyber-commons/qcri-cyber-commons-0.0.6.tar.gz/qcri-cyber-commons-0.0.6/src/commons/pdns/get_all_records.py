import pdns
import sys
import os

def save_all(domain, folder, limit):
    entries = pdns.pdns_domain(domain, None, None, None, None, limit)
    filename = os.path.join(folder, domain)
    fh = open(filename, "w")
    if entries != None:
        for entry in entries:
            fh.write("{}\n".format(entry))
    fh.close()

def all_domains(domainf, folder, limit):
    df = open(domainf)
    for domain in df:
        domain = domain.strip().strip(".").encode("idna").decode()
        save_all(domain, folder, limit)

if __name__ == "__main__":
    domainfile = sys.argv[1]
    outfolder = sys.argv[2]
    limit = int(sys.argv[3])
    all_domains(domainfile, outfolder, limit)

    
