from commons.utils.date_tools import vtdate2epoch


# convert the first entry in VirusTotal WHOIS record (JSON object) into a feature dictionary
# TODO: consider historical WHOIS
def vtwhois2csv(vtj):
    features = dict()
    features['domain'] = None
    features['registrant'] = None
    features['registrar'] = None
    features['creation'] = None
    features['update'] = None
    features['expiration'] = None
    features['ns'] = None
    features['whoiserver'] = None

    try:
        whois_all = vtj["data"]
        if len(whois_all) == 0:
            return features

        # only consider the latest entry
        whois = whois_all[0]

        try:
            domain = whois["attributes"]["whois_map"]["Domain Name"].lower()
        except:
            pass
            # if there are more than 1 whois entry, try the second entry
            if len(whois_all) > 1:
                whois = whois_all[1]
                # if domain name is not available in the second attempt, we will not check further
                try:
                    domain = whois["attributes"]["whois_map"]["Domain Name"].lower()
                except:
                    pass

        features['domain'] = domain

        try:
            features['creation'] = vtdate2epoch(whois["attributes"]["whois_map"]["Creation Date"])
        except:
            pass
            # if there are more than 1 whois entry, try the second entry
            if len(whois_all) > 1:
                whois = whois_all[1]
                try:
                    features['creation'] = vtdate2epoch(whois["attributes"]["whois_map"]["Creation Date"])
                except:
                    pass

        try:
            features['registrant'] = whois["attributes"]["registrant_name"].lower()
        except:
            pass

        try:
            features['registrar'] = whois["attributes"]["whois_map"]["Registrar"].lower()
        except:
            pass
            try:
                features['registrar'] = whois["attributes"]["registrar_name"].lower()
            except:
                pass

        try:
            features['expiration'] = vtdate2epoch(whois["attributes"]["whois_map"]["Registry Expiry Date"])
        except:
            pass

        try:
            features['update'] = vtdate2epoch(whois["attributes"]["whois_map"]["Updated Date"])
        except:
            pass

        try:
            features['ns'] = whois["attributes"]["whois_map"]["Name Server"].lower()
        except:
            pass

        try:
            features['whoiserver'] = whois["attributes"]["whois_map"]["Registrar WHOIS Server"].lower()
        except:
            pass
    except:
        pass
    return features
