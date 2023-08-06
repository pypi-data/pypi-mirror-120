'''
Extract lexical features
'''
import pandas as pd
import tldextract
from urllib.parse import urlparse
import re
import entropy
import math
from Levenshtein import distance
import sys
from brandseg import BrandSeg
from confusables import unconfuse
from suspicious import tlds, popular_keywords


#################################################################################
brands_df = pd.read_csv("pt_alexa_brands_20210108.csv", header = None)
brands_df.columns = ["brand", "domain", "description"]
brands = set(brands_df["brand"].unique())

#################################################################################

#check if a given text corresponds to an IP address
def is_ip(x):
    pat = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
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

#lexical features
def get_lex_features(domain, bseg, brands):
    features = dict()

    #segment the brand
    res = bseg.segment_domain(domain)
    sub_words = res[0]
    dom_words = res[1]
    all_words = sub_words + dom_words
    tld = res[2]

    
    features["domain"] = domain
    # Suspicious TLD
    features["suspicious_tld"] = 0
    for t in tlds:
        if t == tld:
            features["suspicious_tld"] = 1
            break

    # Remove initial '*.' for wildcard certificates bug
    if domain.startswith('*.'):
        domain = domain[2:]

    features["length"] = len(domain)

    # Entropy
    # Higher entropy is kind of suspicious
    features["entropy"] = entropy.shannon_entropy(domain)

    # IDN characters
    domain = unconfuse(domain)

    # Contains embedded TLD/ FAKE TLD
    features["fake_tld"] = 0
    #exclude tld
    for word in all_words:
        if word in ['com', 'net', 'org', 'edu', 'mil', 'gov']:
            features["fake_tld"] += 1

    ## No. of popular brand names appearing in domain name
    #features["brand"] = 0
    #for br in brands:
    #    for word in all_words:
    #        if br in word:
    #            features["brand"] += 1
    
    features["brand_pos"] = -1
    for brand in brands:
        i = domain.find(brand)
        if i >= 0:
            features["brand_pos"] = i
            break

    # Appearance of popular keywords
    features["pop_keywords"] = 0
    for word in popular_keywords:
        if word in all_words:
            features["pop_keywords"] += 1

    # Testing Levenshtein distance for keywords
    # Let's go for Levenshtein distance less than 2
    #features["similar"] = 0
    #for br in brands:
    #    # Removing too generic keywords (ie. mail.domain.com)
    #    for word in [w for w in all_words if w not in ['email', 'mail', 'cloud']]:
    #        if distance(str(word), str(br)) <= 2:
    #            features["similar"] += 1

    # Lots of '-' (ie. www.paypal-datacenter.com-acccount-alert.com)
    features["is_idn"] = 0
    if 'xn--' in domain:
        features["is_idn"] = 1
        features["minus"] = domain.count('-') - 2
    else:
        features["minus"] = domain.count('-')

    # Deeply nested subdomains (ie. www.paypal.com.security.accountupdate.gq)
    #features["num_subdomains"] = domain.count('.') - 1
    
    return features

#a simple test
if __name__ == "__main__":
    print(get_lex_features("www.paypal-datacenter.com-acccount-alert.com", BrandSeg(), brands))
