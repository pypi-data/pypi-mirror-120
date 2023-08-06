import sys
import tldextract
import pandas as pd

def get_phishtank_data(inputfile, outfile):
    inf = open(inputfile)
    data = set()
    for line in inf:
        arr = line.split(',')
        if len(arr) < 2:
            continue
        data.add(arr[0])
        data.add(arr[1])
        ext = tldextract.extract(arr[1])
        data.add(ext.domain + "." + ext.suffix)
    df = pd.DataFrame(data)
    df.to_csv(outfile, header = None, index = False)

get_phishtank_data(sys.argv[1], sys.argv[2])    
