'''
Scraping openphish
'''
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
    chrome_options.add_argument("--headless")
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
    f1 = open(outfile, "w")
    f1.write(response)
    f1.close()

def parse_page(outfile):
    f2 = open(outfile + "_parsed", "a")
    soup = BeautifulSoup(open(outfile).read(), features = "html.parser")
    table = soup.find("table", {"class": "pure-table pure-table-striped"})
    if table != None:
        tbody = table.find("tbody")
        if tbody != None:
            trs = tbody.find_all("tr")
            for tr in trs:
                tds = tr.find_all("td")
                row = []
                for td in tds:
                    row.append(td.text)
                f2.write("{}\n".format("#####".join(row)))
    f2.close()

def save_page(outfile):
    agent_index = math.floor(random.uniform(0, len(USER_AGENTS)))
    browser = start_browser(agent_index)
    try:
        url = "https://openphish.com/"
        save_links(fetch_url(browser, url), outfile + "_raw")
        parse_page(outfile + "_raw")
    except Exception as e:
        print(e)
        pass
    close_browser(browser)

if __name__ == "__main__":
    option = sys.argv[1]
    if option == "page":
        #generic file prefix
        save_page(sys.argv[2])
