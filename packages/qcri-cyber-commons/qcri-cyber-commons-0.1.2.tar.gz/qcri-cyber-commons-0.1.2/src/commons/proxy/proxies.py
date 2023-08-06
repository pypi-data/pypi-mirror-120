import requests

'''
Description: Wrappers to connect to torguard proxies
Author: @nabeelxy
'''

# List of paid proxies listed in torguard as of 20191008
proxy_pnts = ['br', 'chil', 'ca', 'vanc.ca.west', 'cr', 'mx', 'atl.east.usa', 'la.west.usa', 'fl.east.usa',
              'dal.central.usa', 'nj.east.usa', 'ny.east.usa', 'chi.central.usa', 'lv.west.usa', 'sf.west.usa',
              'sa.west.usa', 'aus', 'bl', 'bg', 'bul', 'cp', 'czech', 'den', 'fin', 'fr', 'gr', 'gre', 'hg', 'ice',
              'ire', 'it', 'lv', 'lux', 'md', 'nl', 'no', 'pl', 'por', 'ro', 'slk', 'sp', 'swe', 'swiss', 'turk',
              'ukr', 'uk', 'au', 'hk', 'jp', 'sk', 'my', 'nz', 'singp', 'tw', 'thai', 'egy', 'in', 'isr', 'isr2', 'za',
              'uae']


def get_proxy(proxy_index, username, password):
    return "{0}:{1}@{2}.torguardvpnaccess.com:6060".format(username, password, proxy_pnts[proxy_index])


def get_working_proxies(current_proxy_pnts, username=None, password=None):
    url = 'https://httpbin.org/ip'
    new_proxy_pnts = list()
    for proxy_index in range(0, len(current_proxy_pnts)):
        proxy = get_proxy(proxy_index, username, password)
        try:
            r = requests.get(url, proxies={'http': proxy, 'https': proxy})
            if r.status_code == 200:
                new_proxy_pnts.append(current_proxy_pnts[proxy_index])
            else:
                print("Error: proxy {}".format(current_proxy_pnts[proxy_index]))
        except Exception as e:
            print(e)
            print("Timed out proxy {}".format(current_proxy_pnts[proxy_index]))
            pass
    return new_proxy_pnts


def proxy_exe(url, proxy_index, username=None, password=None, method="get", params=None, data=None, headers=None):
    proxy = get_proxy(proxy_index, username, password)
    try:
        if method == "get":
            res = requests.get(url, proxies={'http': proxy, 'https': proxy}, headers=headers, params=params)
        elif method == "post":
            res = requests.post(url, data=data, proxies={'http': proxy, 'https': proxy}, headers=headers, params=params)
        else:
            print("Unsupported HTTP method: {}".format(method))
            return None
        if res.status_code == 200:
            return res
        else:
            print("Error: proxy {}".format(proxy_pnts[proxy_index]))
    except Exception as e:
        print(e)
        print("Time out: proxy {}".format(proxy_pnts[proxy_index]))
        pass
    return None
