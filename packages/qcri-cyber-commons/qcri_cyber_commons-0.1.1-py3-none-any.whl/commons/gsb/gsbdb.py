import requests
import json
import sys

GSB_FETCH_URL = "https://safebrowsing.googleapis.com/v4/threatListUpdates:fetch"

#minhaj
#api_keys = ['AIzaSyCtXkzebCAfuISFqAog9pep_sSvY1-9SWY']

#digestize
api_keys = ['AIzaSyCXUW2uCTHoSyLjAIEKzNRPUIXCfG3MScU']


def fetch_db(outfile, key_index = 0):
    params = {'apikey': api_keys[key_index]}
    output = "{'Empty': 'Empty'}"
    try:
        req = requests.post(GSB_FETCH_URL, data=params)
        if req.status_code == 200:
            output = req.json()
            if output['response_code'] == -1:
                output['url'] = url
        elif req.status_code == 204:
            output = {'ERROR': 'Received HTTP 204: You may have exceeded the rate limit', 'url':url}
    except requests.ConnectTimeout as e:
        print(e)
        output = {'ERROR': '##timed out', 'url':url}

    of = open(outfile, "w")
    of.write("{}".format(json.dumps(output)))

fetch_db(sys.argv[1])
