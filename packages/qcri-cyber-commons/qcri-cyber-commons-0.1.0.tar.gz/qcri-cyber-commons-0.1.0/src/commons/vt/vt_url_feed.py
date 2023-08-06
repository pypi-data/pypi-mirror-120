import requests
import io
import tarfile
import json
import sys
import os

#Note: this is the private key. We have a rate limit of 1000 queries per day.
#Please use this sparingly as we use this quota to download VT URL feed daily as well 
#APIKEY = '9e9ce9e13e321609fa73ed57d287ccae92986a21647d70c720f1cb9b9ef86c31'

#nabeel academic - valid from 8/5/2020 to 7/11/2020 (6 months)
#20K queries per day
APIKEY = '0b48e71dc148ab5935780bf74b07cadc7049b6684ea4d0bcffbaf5070db4c6bf'

VT_URL_FEED_URL = "https://www.virustotal.com/vtapi/v2/url/feed"

#pkg format is YYYYMMDDTHH
def get_file(pkg, folder):
    querystring = {"apikey": APIKEY, "package": pkg}
    outf = os.path.join(folder, "url-{0}.tar.bz2".format(pkg))
    try:
        response = requests.get(VT_URL_FEED_URL, params=querystring)
        print(len(response.content))
        package_file = open(outf, 'wb')
        package_file.write(response.content)
        package_file.close()
    except Exception as e:
        print(e)
        print("failed: {}".format(pkg))

get_file(sys.argv[1], sys.argv[2])
