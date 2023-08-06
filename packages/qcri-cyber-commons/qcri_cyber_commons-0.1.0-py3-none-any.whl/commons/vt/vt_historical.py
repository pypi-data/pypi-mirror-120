import psycopg2
import sys
from datetime import datetime
import datetime 

user_name = "vtuser"
paswd = "vtuser"
host_name = "10.4.8.73"
port_id = "5432"
database_name = "vt_snapshot"

def get_conn():
    conn = psycopg2.connect(user = user_name,
                            password = paswd,
                            host = host_name,
                            port = port_id,
                            database = database_name)
    return conn

def get_vt_status(db, domain):
    if domain == None or len(domain) == 0:
        print("WARNING: Empty domain")
        return None

    c = db.cursor()
    params = (domain, )
    query = "SELECT domain, first_detected, last_detected, malcount, suscount FROM vt WHERE domain = %s"
    c.execute(query, params)
    record = c.fetchone()
    if record != None:
        record = list(record)
        record[1] = record[1].strftime("%Y%m%d")
        record[2] = record[2].strftime("%Y%m%d")
    c.close()
    return record 

def get_vt_status_file(db, infile, outfile):
    of = open(outfile, "w")
    inf = open(infile)

    for domain in inf:
        domain = domain.strip()
        res = get_vt_status(db, domain)
        if res == None:
            of.write("{} {}\n".format(domain, "##NOTFOUND##"))
        else:
            res2 = [str(s) for s in res]
            of.write("{}\n".format(" ".join(res2)))
    of.close()

if __name__ == "__main__":
    db = get_conn()
    if db != None:
        if sys.argv[1] == "domain_lookup":
            print(get_vt_status(db, sys.argv[2]))
        elif sys.argv[1] == "file_lookup":
            get_vt_status_file(db, sys.argv[2], sys.argv[3])
        else:
            print("Unsupported option")
        db.close()
