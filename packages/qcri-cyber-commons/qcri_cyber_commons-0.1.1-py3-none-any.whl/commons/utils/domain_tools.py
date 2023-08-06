import tldextract
from urllib.parse import urlparse
import re

#check if a given text corresponds to an IP address
def is_ip(x):
    pat = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    if pat.match(x):
        return True
    return False

def contains_ip(x):
    pat = re.compile(".*\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}.*")
    if pat.match(x):
        return True
    return False

def get_2ld(fqdn, part = "apex"):
    try:
        ext = tldextract.extract(fqdn)
        if len(ext.domain) == 0 or len(ext.suffix) == 0:
            return None
        else:
            if part == "tld":
                return ext.suffix
            elif part == "domain":
                return ext.domain
            else: 
                return ext.domain + "." + ext.suffix
    except Exception as e:
        #print("ERROR - something wrong with the FQDN: {}".format(fqdn))
        #print(e)
        pass
    return None

def get_fqdn(url):
    try:
        uri = urlparse(url)
        if uri != None:
            return uri.netloc
    except Exception as e:
        pass
    return None

def get_path(url):
    try:
        uri = urlparse(url)
        if uri != None:
            return uri.path
    except Exception as e:
        pass
    return None

def get_query(url):
    try:
        uri = urlparse(url)
        if uri != None:
            return uri.query
    except Exception as e:
        pass
    return None

def get_scheme(url):
    try:
        uri = urlparse(url)
        if uri != None:
            return uri.scheme
    except Exception as e:
        pass
    return None
