import vt_query_host as vtq
import sys
def get_set(filename):
    words = set()
    fn = open(filename)
    for word in fn:
        words.add(word.strip())
    return words

def ext_features(infilename, outfilename):
    infile = open(infilename)
    outfile = open(outfilename, "w+")

    for domain in infile:
        domain = domain.strip()
        record = vtq.get_record(domain, "vt_ts")
        if record == None:
            continue
        lifetime = record[1] - record[0]
        total_count = record[2]    
        mal_count = record[3]
        ratio = float(mal_count)/total_count
        outfile.write("{} {} {} {} {}\n".format(domain, lifetime, total_count, mal_count, ratio))
    outfile.close()

if __name__ == "__main__":
    ext_features(sys.argv[1], sys.argv[2])
