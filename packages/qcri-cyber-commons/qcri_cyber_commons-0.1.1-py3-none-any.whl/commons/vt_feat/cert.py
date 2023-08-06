from cert_oid import oid_dv, oid_ov, oid_ev, oid_iv

from commons.utils.date_tools import vtdate2epoch


def find_validity_type(cert):
    try:
        cert_policies = cert["attributes"]["extensions"]["certificate_policies"]
        for p in cert_policies:
            if p in oid_dv:
                return 'DV'
            elif p in oid_ov:
                return 'OV'
            elif p in oid_ev:
                return 'EV'
            elif p in oid_iv:
                return 'IV'
    except KeyError as e:
        pass

    try:
        subject_o = cert["attributes"]["subject"]["O"]
        if subject_o != None and "domain control validated" in subject_o.lower():
            return 'DV'
    except KeyError as e:
        pass
        # subject organization is not persent meaning it is not O or E validated
        return 'DV'

    try:
        issuer_o = cert["attributes"]["issuer"]["O"]
        if issuer_o != None and ("domain control validated" in issuer_o.lower() or \
                                 "let's encrypt" in issuer_o.lower()):  # Let's Encrypt only produce DV
            return 'DV'
    except KeyError as e:
        pass

    return 'NA'


# Extract features from the VirusTotal certificates (JSON)
# TODO: consider historical features
def vtcert2csv(vtj):
    features = dict()
    features['subject'] = None
    features['issuer'] = None
    features['creation'] = None
    features['expiration'] = None
    features['san'] = None
    features['type'] = None

    try:
        cert_all = vtj["data"]
        if len(cert_all) == 0:
            return features

        # only consider the latest entry
        cert = cert_all[0]

        try:
            features['subject'] = cert["attributes"]["subject"]["CN"].strip()
        except KeyError as e:
            pass

        try:
            features['issuer'] = cert["attributes"]["issuer"]["O"].strip()
        except KeyError as e:
            pass

        try:
            features['creation'] = vtdate2epoch(cert["attributes"]["validity"]["not_before"].strip())
        except KeyError as e:
            pass

        try:
            features['expiration'] = vtdate2epoch(cert["attributes"]["validity"]["not_after"].strip())
        except KeyError as e:
            pass

        try:
            features['san'] = cert["attributes"]["extensions"]["subject_alternative_name"]
        except KeyError as e:
            pass

        features['type'] = find_validity_type(cert)
    except KeyError as e:
        pass
    return features
