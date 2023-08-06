"""
This python script is used to check urls against google safe browser API. This scripts takes a input file of urls and
check those urls against google safe browser API.
Usage: python gsb_process.py <input file> 
Output: output will a file in same directory as input with name as <input file>_output. Each line of output file will be
 url and status of url e.g True for malicious status and False for Benign status
"""

import json
import sys

import requests

proxy_pnts = ['au', 'melb.au', 'bul', 'cp', 'egy', 'iom', 'isr', 'fin', 'br', 'ca', 'vanc.ca.west', 'frank.gr', 'ice',
              'ire', 'in', 'jp', 'nl', 'uk', 'lon.uk', 'ro', 'ru', 'mos.ru', 'swe', 'swiss', 'bg', 'hk', 'cr', 'hg',
              'ind', 'my', 'thai', 'turk', 'tun', 'mx', 'singp', 'saudi', 'fr', 'pl', 'czech', 'gre', 'it', 'sp', 'no',
              'por', 'za', 'den', 'vn', 'pa', 'sk', 'cn', 'lv', 'lux', 'nz', 'md', 'uae', 'slk', 'fl.east.usa',
              'atl.east.usa', 'ny.east.usa', 'chi.central.usa', 'dal.central.usa', 'la.west.usa', 'lv.west.usa',
              'sa.west.usa', 'nj.east.usa', 'central.usa', 'centralusa', 'west.usa', 'westusa', 'east.usa', 'eastusa']

result = dict()
api_key = ""
final_result = dict()


def main():
    global final_result
    global api_key
    input_urls, url_dict = get_url_list(inpf)
    for key in url_dict:
        api_key = api_keys[key]
        proxy = get_proxy(key)
        proxy_dict = {'http': proxy}
        clientId = "qcri_{}".format(key)
        lookup_urls_all(clientId, url_dict[key], proxy_dict)

    outf = "{0}.gsb".format(inpf)
    with open(outf, 'w+', encoding='utf-8') as f:
        for key in final_result:
            f.write("{} {}\n".format(key, final_result[key]))


def get_url_list(inpf):
    input_urls = set()
    url_dict = {}
    index = 0
    block = 10000  # in practice, this value should be 10000

    with open(inpf, encoding='utf-8') as f:
        for line in f:
            input_urls.add(line.strip())

    print("total unique urls: {}".format(len(input_urls)))
    url_list = list(input_urls)

    for i in range(0, len(url_list), block):
        if index == len(api_keys):
            break
        url_dict[index] = url_list[i:i + block]
        index += 1

    return input_urls, url_dict


def get_proxy(proxy_index):
    return "{0}:{1}@{2}.torguardvpnaccess.com:6060".format(username, password, proxy_pnts[proxy_index])


def lookup_urls_all(clientId, urls, proxy_dict):
    global final_result
    sub_block = 10  # in practical use this value shoud be 500
    for i in range(0, len(urls), sub_block):
        res = lookup_urls(clientId, urls[i:i + sub_block], proxy_dict)
        if res is not None:
            for key in res:
                final_result[key] = res[key]


def lookup_urls(clientId, urls, proxy_dict):
    global result
    global api_key

    data = {
        "client": {
            "clientId": clientId,
            "clientVersion": "0.1"
        },
        "threatInfo": {
            "threatTypes":
                [
                    "MALWARE",
                    "SOCIAL_ENGINEERING",
                    "THREAT_TYPE_UNSPECIFIED",
                    "UNWANTED_SOFTWARE",
                    "POTENTIALLY_HARMFUL_APPLICATION"
                ],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{'url': u} for u in urls]
        }
    }
    headers = {'Content-type': 'application/json'}

    r = requests.post(
        'https://safebrowsing.googleapis.com/v4/threatMatches:find',
        data=json.dumps(data),
        params={'key': api_key},
        headers=headers,
        proxies=proxy_dict
    )
    if r.status_code == 200:
        # Return clean results
        if r.json() == {}:
            return dict([(u, {"malicious": False}) for u in urls])
        else:
            for url in urls:
                # Get matches
                matches = [match for match in r.json()['matches'] if match['threat']['url'] == url]
                if len(matches) > 0:
                    result[url] = {
                        'malicious': True,
                        'platforms': list(set([b['platformType'] for b in matches])),
                        'threats': list(set([b['threatType'] for b in matches])),
                        'cache': min([b["cacheDuration"] for b in matches])
                    }
                else:
                    result[url] = {"malicious": False}
            return result
    else:
        print("Some error has occurred while using google safe broswer POST api. Status code: {}".format(r.status_code))


if __name__ == '__main__':
    if len(sys.argv) == 4:
        inpf, username, password, api_keys = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
        main()
    else:
        print("Usage: python gsb_process.py <input file>")
