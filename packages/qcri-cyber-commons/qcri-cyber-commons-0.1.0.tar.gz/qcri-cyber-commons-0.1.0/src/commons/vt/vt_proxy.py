import json
import os
import sys
import time
from datetime import datetime
from multiprocessing.pool import ThreadPool

from commons.proxy import proxies

'''
Description: Scan and collect VT results using public keys
We use a proxy implementation to do the scanning in parallel
Author: @nabeelxy
'''
VT_SCAN_URL = 'https://www.virustotal.com/vtapi/v2/url/scan'
VT_REPORT_URL = 'https://www.virustotal.com/vtapi/v2/url/report'


def load_keys(keyfile):
    keys = list()
    with open(keyfile) as kf:
        for line in kf:
            keys.append(line.strip())
    return keys


def scan_proxy(url, key, index):
    data = {'apikey': key, 'url': url}
    req = proxies.proxy_exe(VT_SCAN_URL, index, proxies.proxy_pnts, "post", None, data)
    if req == None:
        return {'ERROR': 'None Returned'}
    return req.json()


def report_proxy(resource, key, index):
    data = {'apikey': key, 'resource': resource}
    req = proxies.proxy_exe(VT_REPORT_URL, index, proxies.proxy_pnts, "post", None, data)
    if req == None:
        return {'ERROR': 'None Returned'}
    return req.json()


def scan_thread(domainlist, index, key, folder):
    results = list()
    of = open(os.path.join(folder, "part_" + str(index)), "w+")
    for domain in domainlist:
        domain = domain.strip()
        result = json.dumps(scan_proxy(domain, key, index))
        results.append(result)
        of.write("{}\n".format(result))
        time.sleep(16)  # VT public allows only 4 queries per minute
    of.close()
    print("Thread {} Done".format(index))
    return results


def report_thread(scanidlist, index, key, folder):
    results = list()
    of = open(os.path.join(folder, "part_" + str(index)), "w+")
    for scanid in scanidlist:
        result = json.dumps(report_proxy(scanid, key, index))
        of.write("{}\n".format(result))
        results.append(result)
        time.sleep(16)  # VT public allows only 4 queries per minute
    of.close()
    return results


# number of threads = number of keys
# assumes that number of proxies >= number of keys
# TODO: improvement - handle the case where the number of proxies are less than
# the number of keys - implement proxy rotation
def run_threads(inputfile, outputfile, keys, method):
    inputlist = list()
    if method == "scan":
        with open(inputfile) as df:
            for line in df:
                try:
                    inputlist.append(line.strip())
                except TypeError as e:
                    pass
    elif method == "report":
        with open(inputfile) as sf:
            for line in sf:
                json_obj = json.loads(line)
                try:
                    scan_id = json_obj['scan_id'].strip()
                    inputlist.append(scan_id)
                except KeyError as e:
                    pass
                except TypeError as e2:
                    pass
    else:
        print("Unsupported method {}".format(method))
        return

    num_threads = len(keys)
    block_size = int(len(inputlist) / num_threads)
    all_results = list()
    pool = ThreadPool(num_threads)
    folder = datetime.today().strftime('%Y%m%d%H%M')

    if not os.path.exists(folder):
        os.makedirs(folder)

    for t in range(num_threads):
        start = t * block_size
        end = (t + 1) * block_size
        if t == num_threads - 1:
            end = len(inputlist)
        print("starting proxy {} key {} proxy {} items {}".format(t, keys[t], proxies.proxy_pnts[t],
                                                                  len(inputlist[start:end])))
        if method == "scan":
            all_results += [pool.apply_async(scan_thread,
                                             kwds={'domainlist': inputlist[start:end], 'index': t, 'key': keys[t],
                                                   'folder': folder})]
        else:
            all_results += [pool.apply_async(report_thread,
                                             kwds={'scanidlist': inputlist[start:end], 'index': t, 'key': keys[t],
                                                   'folder': folder})]
    pool.close()
    pool.join()

    of = open(outputfile, "w+")
    for result in all_results:
        outputlist = result.get()
        for line in outputlist:
            of.write("{}\n".format(line))
    of.close()
    print("All Done")


if len(sys.argv) < 5:
    print("Usage: {} method [scan|report] key_file input_file output_file".format(sys.argv[0]))
    exit()

method = sys.argv[1]  # scan or report
keys = load_keys(sys.argv[2])
domainfile = sys.argv[3]
outputfile = sys.argv[4]
run_threads(domainfile, outputfile, keys, method)
