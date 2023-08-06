import pandas as pd

public_df = pd.read_csv("/export/sec02/nabeel/Common/pub/public_apex_domains_20201127", header = None)
public_df.columns = ['domain']
public_domains = set(public_df['domain'].unique())

def is_public(apex):
    global public_domains
    if apex in public_domains:
        return True
    return False
