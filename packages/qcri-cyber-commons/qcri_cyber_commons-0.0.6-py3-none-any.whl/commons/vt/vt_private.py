import requests

VT_SCAN_URL = 'https://www.virustotal.com/vtapi/v2/url/scan'
VT_REPORT_URL = 'https://www.virustotal.com/vtapi/v2/url/report'
VT_DOMAIN = 'https://www.virustotal.com/api/v3/domains/{}/{}'
VT_IP = 'https://www.virustotal.com/api/v3/ip_addresses/{}/{}'
VT_FILE = 'https://www.virustotal.com/api/v3/files/{}/{}'


def scan(url, api_keys, key_index=0):
    params = {'apikey': api_keys[key_index], 'url': url}
    output = {}
    try:
        req = requests.post(VT_SCAN_URL, data=params)
        if req.status_code == 200:
            output = req.json()
            if output['response_code'] == -1:
                output['url'] = url
        elif req.status_code == 204:
            output = {'ERROR': 'Received HTTP 204: You may have exceeded the rate limit', 'url': url}
    except requests.ConnectTimeout as e:
        output = {'ERROR': '##timed out', 'url': url}
    return output


def getReport(resource, api_keys, key_index=0):
    params = {'apikey': api_keys[key_index], 'resource': resource, 'allinfo': 'true'}
    output = {}
    try:
        req = requests.get(VT_REPORT_URL, params=params)
        if req.status_code == 200:
            output = req.json()
        elif req.status_code == 204:
            output = {'ERROR': 'Received HTTP 204: You may have exceeded the rate limit', 'url': resource}
    except requests.ConnectTimeout as e:
        output = {'ERROR': '##timed out', 'url': resource}
    return output


def getDomain(domain, relationship, api_keys, key_index=0, limit=None):
    querystring = None
    url = VT_DOMAIN.format(domain, relationship)
    output = {}
    if limit != None:
        querystring = {"limit": "{}".format(limit)}
    try:
        headers = {'x-apikey': api_keys[key_index]}
        response = requests.request("GET", url, headers=headers, params=querystring)
        if response.status_code == 200:
            output = response.json()
        else:
            output = {'ERROR': 'Received HTTP Code <> 200'}
    except requests.ConnectTimeout as e:
        output = {'ERROR': '##timed out', 'url': url}
    return output


def getIP(ip, relationship, api_keys, key_index=0, limit=None):
    querystring = None
    url = VT_IP.format(ip, relationship)
    output = {}
    if limit != None:
        querystring = {"limit": "{}".format(limit)}
    try:
        headers = {'x-apikey': api_keys[key_index]}
        response = requests.request("GET", url, headers=headers, params=querystring)
        if response.status_code == 200:
            output = response.json()
        else:
            output = {'ERROR': 'Received HTTP Code <> 200'}
    except requests.ConnectTimeout as e:
        output = {'ERROR': '##timed out', 'url': url}
    return output


def getFile(hashf, relationship, api_keys, key_index=0, limit=None):
    querystring = None
    url = VT_FILE.format(hashf, relationship)
    output = {}
    if limit != None:
        querystring = {"limit": "{}".format(limit)}
    try:
        headers = {'x-apikey': api_keys[key_index]}
        response = requests.request("GET", url, headers=headers, params=querystring)
        if response.status_code == 200:
            output = response.json()
        else:
            output = {'ERROR': 'Received HTTP Code <> 200: {}'.format(response.status_code)}
    except requests.ConnectTimeout as e:
        output = {'ERROR': '##timed out', 'url': url}
    return output
