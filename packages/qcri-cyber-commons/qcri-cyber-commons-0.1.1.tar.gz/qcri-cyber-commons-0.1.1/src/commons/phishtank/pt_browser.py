from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import tldextract
from urllib.parse import urlparse
import time
import random
from bs4 import BeautifulSoup
import sys
import os
import math
import glob

USER_AGENTS = [
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
"Mozilla/5.0 (iPhone; CPU iPhone OS 13_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/83.0.4147.71 Mobile/15E148 Safari/604.1",
"Mozilla/5.0 (iPad; CPU OS 13_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/83.0.4147.71 Mobile/15E148 Safari/604.1",
"Mozilla/5.0 (iPod; CPU iPhone OS 13_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/83.0.4147.71 Mobile/15E148 Safari/604.1",
"Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Mobile Safari/537.36",
"Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Mobile Safari/537.36"
]

def get_2ld(fqdn, only_tld = False):
    try:
        ext = tldextract.extract(fqdn)
        if len(ext.domain) == 0 or len(ext.suffix) == 0:
            return None
        else:
            if only_tld:
                return ext.suffix
            else: 
                return ext.domain + "." + ext.suffix
    except Exception as e:
        pass
    return None

def get_fqdn(url):
    try:
        uri = urlparse(url)
        if uri != None:
            return uri.netloc
    except Exception as e:
        pass

def start_browser(agent_index):
    #brew cask install chromedriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument('user-agent="{}"'.format(USER_AGENTS[agent_index]))
    browser = webdriver.Chrome(executable_path=r"chromedriver", options=chrome_options)

    browser.set_page_load_timeout(10)

    return browser

def fetch_url(browser, url):
    try:
        browser.get(url)
        return browser.page_source
    except Exception as e:
        return "<html>Error: {}</html>".format(e) 

def close_browser(browser):
    browser.close()

def save_links(response, outfile):
    f1 = open(outfile, "a", encoding = 'utf-8')
    f1.write(response)
    f1.close()

def parse_page(outfile):
    f2 = open(outfile + "_parsed", "w", encoding = 'utf-8')
    soup = BeautifulSoup(open(outfile).read(), features = "html.parser")
    table = soup.find("table")
    if table != None:
        trs = table.find_all("tr")
        for tr in trs:
            tds = tr.find_all("td")
            row = []
            for td in tds:
                row.append(td.text)
            f2.write("{}\n".format("#####".join(row)))
    f2.close()

def extract_url(res):
    soup = BeautifulSoup(res, features = "html.parser")
    span = soup.find("span", {"style":"word-wrap:break-word;"})
    if span != None:
        b = span.find("b")
        if b != None:
            return b.text
    return None

def collect_urls(parsed_file, last_phishid):
    pf = open(parsed_file, encoding = 'utf-8')
    outf = open(parsed_file + "_fullurls", "w", encoding = 'utf-8')
    agent_index = math.floor(random.uniform(0, len(USER_AGENTS)))
    browser = start_browser(agent_index)
    highest_phishid = -1
    for line in pf:
        wt = random.uniform(3, 6)
        arr = line.split("#####")
        if len(arr) != 5:
            continue
        try:
            phishid = int(arr[0])
            if phishid > highest_phishid:
                highest_phishid = phishid
        except:
            pass
            continue
        #only collect those phishing urls that are not collected previously
        if phishid <= last_phishid:
            continue

        url = arr[1]
        if "SPAM-TO-BE-DELETED" in url:
            continue
        #... means that the full URL is not availble
        if "..." in url:
            time.sleep(wt)
            lookup = "http://phishtank.org/phish_detail.php?phish_id={}".format(phishid)
            res = fetch_url(browser, lookup)
            if res != None:
                full_url = extract_url(res)
            print("{}#####{}".format(phishid, full_url))
            outf.write("{}#####{}\n".format(phishid, full_url))
    outf.close()
    close_browser(browser)
    return highest_phishid
    
def save_page(outfile, pages, phishidfile):
    agent_index = math.floor(random.uniform(0, len(USER_AGENTS)))
    browser = start_browser(agent_index)
    last_phishid = int(open(phishidfile).read().strip())
    for page in range(0, pages):
        wt = random.uniform(5, 10)
        try:
            #Try not to annnoy Google, with a random short wait
            url = "http://phishtank.org/phish_search.php?page={}".format(page)
            new_filename = outfile + "_" + str(page) + "_raw"
            save_links(fetch_url(browser, url), new_filename)
            parse_page(new_filename)
            phishid = -1
            try:
                phishid = collect_urls(new_filename + "_parsed", last_phishid)
            except:
                print("url parsing error")
                print(e)
                pass

            #write the latest phish id for the current lookup
            if page == 0:
                if phishid == -1:
                    print("ERROR: Highest phish id cannot be -1")
                else:
                    pid_f = open(phishidfile, "w")
                    pid_f.write("{}".format(phishid))
                    pid_f.close()
            process_urls(new_filename + "_parsed", last_phishid)
            #don't collect already collected ones
            if phishid <= last_phishid:
                break
            time.sleep(wt)
        except Exception as e:
            print(e)
            pass
    close_browser(browser)

#parse page and collect truncated URLs
def collect_all_urls(outfile):
    for filepath in glob.iglob(outfile + '_*_raw'):
        parse_page(filepath)
        collect_urls(filepath + "_parsed")

def process_urls(parsed_file, last_phishid):
    pf = open(parsed_file, encoding = 'utf-8')
    uf = open(parsed_file + "_fullurls", encoding = 'utf-8')
    ff = open(parsed_file + "_processed", "w", encoding = 'utf-8')

    #load URLs
    full = dict()
    for line in uf:
        arr = line.split("#####")
        if len(arr) != 2:
            continue
        full[arr[0]] = arr[1].strip()

    #process each row
    for line in pf:
        arr = line.strip().split("#####")
        if len(arr) != 5:
            continue
        phishid = arr[0]

        #don't collect urls that are already collected
        try:
            if int(phishid) <= last_phishid:
                continue
        except:
            pass
            continue

        url = arr[1]
        if len(url.strip()) == 0:
            continue
        submitted = "None"
        i = url.find("added on")
        if i != -1:
            submitted = url[i + 9 :]
        if "SPAM-TO-BE-DELETED" in url:
            continue
        #... means that the full URL is not availble
        if "..." in url and phishid in full:
            url = full[phishid]
        else:
            if i != -1:
                url = url[:i]
        if "by" in arr[2]:
            arr[2] = arr[2][3:]

        ff.write("{}\n".format("#####".join([phishid, url, submitted, arr[2], arr[3], arr[4]])))
    ff.close()

#produce a proper csv of the phishtank file    
#def process_all_urls(outfile):
#    for filepath in glob.iglob(outfile + '_*_raw_parsed'):
#        process_urls(filepath)

def aggregate_processed(outfile):
    bdir = os.path.dirname(outfile)
    os.system("cat {}_*_raw_parsed_processed >> {}_all".format(outfile, outfile))
    os.system("mv {}_*_raw_parsed_processed {}/tmp".format(outfile, bdir))
    os.system("cat {}_*_raw_parsed >> {}_raw_parsed".format(outfile, outfile))
    os.system("mv {}_*_raw_parsed {}/tmp".format(outfile, bdir))
    os.system("cat {}_*_raw >> {}_raw".format(outfile, outfile))
    os.system("mv {}_*_raw {}/tmp".format(outfile, bdir))
    os.system("cat {}_*_raw_parsed_fullurls >> {}_raw_parsed_fullurls".format(outfile, outfile))
    os.system("mv {}_*_raw_parsed_fullurls {}/tmp".format(outfile, bdir))

#later check phishing urls
def check_phish(url):
    full_url = "https://checkurl.phishtank.com/checkurl/index.php?url={}".format(url)
    #TODO - implement

if __name__ == "__main__":
    option = sys.argv[1]
    if option == "page":
        #generic file prefix, number of pages, phish_id page
        save_page(sys.argv[2], int(sys.argv[3]), sys.argv[4])
        aggregate_processed(sys.argv[2])
