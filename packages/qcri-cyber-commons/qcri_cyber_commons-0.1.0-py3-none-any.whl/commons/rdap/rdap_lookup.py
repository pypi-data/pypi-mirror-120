'''
Domain/IP/AS lookup using RDAP service
Reference: https://about.rdap.org/
Rate limit: below 10 queries per second
'''
import requests
import sys
import time

#type (domain, ip, autnum)
ENDPOINT = 'https://rdap.org/{}/{}'

#rdap lookup
def rdap_get(rtype, value):
    try:
        req = requests.get(ENDPOINT.format(rtype, value))
        if req.status_code == 200:
            output = req.json()
        elif req.status_code == 204:
            output = {'ERROR': 'Received HTTP 204: You may have exceeded the rate limit', 'url':url}
    except requests.ConnectTimeout as e:
        output = {'ERROR': '##timed out', 'url':url}
    return output

#file lookup
def rdap_get_file(rtype, inputf, outputf, interval = 0.15):
    inf = open(inputf)
    outf = open(outputf, "w")
    for line in inf:
        outf.write("{}\n".format(rdap_get(rtype, line.strip())))
        time.sleep(interval)
    outf.close()
        
if __name__ == "__main__":
    #print(rdap_get(sys.argv[1], sys.argv[2]))
    if len(sys.argv) < 4:
        print("Usage: {} rtype inputfile outputfile".format(sys.argv[0]))
        exit()
    rdap_get_file(sys.argv[1], sys.argv[2], sys.argv[3])
