"""
Get all phishtank URLs collected so far and do a full VT scan
"""
import glob
import pandas as pd
import os
import sys

VT_SRC_PATH = "/export/sec02/nabeel/COVID19-MAL/src/vt"

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

def vt_all_urls(folder, datestr):
    all_urls = set()
    for filepath in glob.iglob('{}/fs_????????'.format(folder)):
        urls = set()
        with open(filepath, encoding = 'utf-8') as fh:
            for line in fh:
                urls.add(line.strip())
        all_urls = all_urls | urls

    splits = list(chunks(list(all_urls), 9000))
    count = 0
    for split in splits:
        filename = "{}/all_{}.{}".format(folder, datestr, count)
        with open(filename, 'w', encoding = 'utf-8') as fh:
            for item in split:
                fh.write("{}\n".format(item))
        count += 1
    
    #currently we only have 5 academic keys to process
    #this dirty hack is added to limit
    if count > 5:
        count = 5

    for i in range(0,count):
        #k = 4 - i
        #k = i
        filename = "{}/all_{}.{}".format(folder, datestr, i)
        os.system("nohup python {}/vt_file.py {} {}.scan {} &".format(VT_SRC_PATH, filename, filename, k))

if __name__ == "__main__":
    vt_all_urls(sys.argv[1], sys.argv[2])
