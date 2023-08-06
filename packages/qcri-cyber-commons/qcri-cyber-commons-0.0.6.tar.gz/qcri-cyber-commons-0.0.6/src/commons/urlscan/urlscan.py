"""
Description: Scanning URLs in urlscan.io and obtaining report, screenshot and dom
"""
import json
import shutil
import sys
import time
from urllib.parse import urlparse

import requests

SPEED_SCAN = 8
SPEED_REPORT = 1


def get_fqdn(url):
    try:
        uri = urlparse(url)
        if uri:
            return uri.netloc
    except Exception as e:
        pass


def scan_url(url, key):
    try:
        headers = {'API-Key': key, 'Content-Type': 'application/json'}
        data = {"url": url, "visibility": "public"}
        response = requests.post('https://urlscan.io/api/v1/scan/', headers=headers, data=json.dumps(data))
        if response != None:
            return response.json()
        else:
            return {"ERROR": url}
    except requests.ConnectTimeout as e:
        return {'ERROR': '##timed out', 'url': url}


def get_report(url, key):
    try:
        headers = {'API-Key': key, 'Content-Type': 'application/json'}
        response = requests.get(url, headers=headers)
        if response:
            return response.json()
        else:
            return {"ERROR": url}
    except requests.ConnectTimeout as e:
        return {'ERROR': '##timed out', 'url': url}


# curl https://urlscan.io/screenshots/$uuid.png
def get_screenshot(uuid, key, folder):
    url = "https://urlscan.io/screenshots/{}.png".format(uuid)
    headers = {'API-Key': key}
    try:
        response = requests.get(url, stream=True, headers=headers)
        with open('{}/{}.png'.format(folder, uuid), 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
    except Exception as e:
        pass


# curl https://urlscan.io/dom/$uuid/
def get_dom(uuid, key, folder):
    url = "https://urlscan.io/dom/{}/".format(uuid)
    headers = {'API-Key': key}
    try:
        response = requests.get(url, headers=headers)
        with open('{}/{}.html'.format(folder, uuid), 'wb') as out_file:
            out_file.write(response.content)
    except Exception as e:
        pass


def scan_file(domain_file, outfile, key):
    of = open(outfile, "w+", encoding='utf-8')
    with open(domain_file, encoding='utf-8') as df:
        for line in df:
            time.sleep(SPEED_SCAN)
            line = line.strip()
            if line.startswith("http"):
                domain = line
            else:
                domain = "https://" + line
            try:
                of.write("{}\n".format(json.dumps(scan_url(domain, key))))
            except Exception as e:
                pass
    of.close()


def report_file(scanid_file, outfile, key, outfolder):
    of = open(outfile, "w+", encoding='utf-8')
    with open(scanid_file, encoding='utf-8') as sf:
        for str in sf:
            json_obj = json.loads(str)
            try:
                time.sleep(SPEED_REPORT)
                if json_obj["message"] == "Submission successful":
                    of.write("{}\n".format(json.dumps(get_report(json_obj["api"], key))))
                get_screenshot(json_obj["uuid"], key, outfolder)
                get_dom(json_obj["uuid"], key, outfolder)
            except KeyError as e:
                pass
    of.close()


def get_scanned_domains(infile, outfile):
    of = open(outfile, "w+", encoding='utf-8')
    with open(infile, encoding='utf-8') as sf:
        for str in sf:
            json_obj = json.loads(str)
            try:
                if json_obj["message"] == "Submission successful":
                    of.write("{}\n".format(get_fqdn(json_obj["url"])))
                elif json_obj["message"] == "DNS Error - Could not resolve domain":
                    of.write("{}\n".format(json_obj["description"].split()[2]))
            except KeyError as e:
                pass
    of.close()


if __name__ == "__main__":
    option = sys.argv[1]
    if option == "scan":
        # url file, #scan output file, #key index
        scan_file(sys.argv[2], sys.argv[3], 0)
    elif option == "report":
        # scan output file, report output file, key index, output folder
        report_file(sys.argv[2], sys.argv[3], 0, sys.argv[4])
    elif option == "both":
        # url file, #scan output file, #report key index, ouput file
        scan_file(sys.argv[2], sys.argv[3], 0)
        report_file(sys.argv[3], sys.argv[4], 0, sys.argv[5])
    elif option == "scanned_domains":
        get_scanned_domains(sys.argv[2], sys.argv[3])

# get_screenshot("27f74f26-a5a4-4199-90ad-2608b3394545", 0, "images")
# get_dom("27f74f26-a5a4-4199-90ad-2608b3394545", 0, "html")
