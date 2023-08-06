import vt_query_host as vtq
import sys
import tldextract
import entropy

def get_set(filename):
    words = set()
    fn = open(filename)
    for word in fn:
        words.add(word.strip())
    return words

def ext_features(infilename, outfilename, keywordfile):
    infile = open(infilename)
    outfile = open(outfilename, "w+")

    keywords = get_set(keywordfile)

    for domain in infile:
        domain = domain.strip()
        record = vtq.get_record(domain, "vt_nod")
        if record == None:
            continue
        lifetime = record[1] - record[0]
        total_count = record[2]    
        mal_count = record[3]
        ratio = float(mal_count)/total_count
        fqdns = record[4].split('##')
        no_fqdns = len(fqdns)
        keyword_count = 0
        dot_count = 0
        sentropy = 0.0
        for fqdn in fqdns:
            ext = tldextract.extract(fqdn)
            if ext.subdomain != None and len(ext.subdomain) > 0:
                dot_count += ext.subdomain.count('.')
                if ext.subdomain in keywords:
                    keyword_count += 1
                sentropy += entropy.shannon_entropy(ext.subdomain)
        outfile.write("{} {} {} {} {} {} {} {} {} {}\n".format(domain, lifetime, total_count, mal_count, ratio, no_fqdns, keyword_count, float(keyword_count)/no_fqdns, float(dot_count)/no_fqdns, float(sentropy)/no_fqdns))
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
    if len(sys.argv) < 4:
        print("{} input-domain-file output-feature-file top-keywords-file".format(sys.argv[0]))
        exit()
    ext_features(sys.argv[1], sys.argv[2], sys.argv[3])
