'''
Description: Get the aggregated VT record for a domain
Note: All time is taken as UTC time
'''
import sys
import psycopg2
import myutils
from datetime import datetime

def get_db_conn(db, user, passwd, host, port):
    conn = None
    try:
        conn = psycopg2.connect(database=db, user=user, password=passwd, host=host, port=port)
        return conn
    except Exception as e:
        print (e)
        pass
        return None

def get_record_(host, db, user, passwd, dbhost, port):
    conn = get_db_conn(db, user, passwd, dbhost, port)
    if conn == None:
        return None

    table = myutils.get_table(host)
    stmt = "SELECT firstseen, lastseen, count, mal_count, ts FROM " + table + " WHERE domain = %s"
    if table != None:
        params = (host,)
        try:
            cur = conn.cursor()
            cur.execute(stmt, params)
            return cur.fetchone()
        except Exception as e:
            print (e)
            pass
            return None
    else:
        return None

#returns an array (firstseen, lastseen, #queries, #mal_count, #timeseries)
def get_record(host, database):
    return get_record_(host, database, "pdns", "pdns", "10.4.8.61", 5432)

def format_record(mode, record):
    fr = ""
    if record != None:
        if mode == 'pretty':
            fr += "Domain: {}\n".format(sys.argv[1])
            fr += "Firstseen: {}\n".format(datetime.fromtimestamp(record[0]).strftime('%Y-%m-%d %H:%M:%S'))
            fr += "Lastseen: {}\n".format(datetime.fromtimestamp(record[1]).strftime('%Y-%m-%d %H:%M:%S'))
            fr += "Total count: {}\n".format(record[2])
            fr += "Mal count: {}\n".format(record[3])
            arr = record[4].split('##')
            ts = dict()
            for entry in arr:
                arr2 = entry.split()
                ts[arr2[0]] = arr2[1]
            count_str = ""
            for key, value in sorted(ts.items()):
                count_str += "{} ".format(value)
            fr += "Counts: {}".format(count_str)
        elif mode == 'csv':
            fr = "{},{},{},{},{},{}".format(sys.argv[1], record[0], record[1], record[2], record[3], record[4])
    return fr

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: {} <domain-name> <format [pretty|csv]> [database]".format(sys.argv[0]))
        exit()

    database = "vt_ts"
    if len(sys.argv) == 4:
        database = sys.argv[3].strip()

    record = get_record(sys.argv[1].strip(), database)
    print(format_record(sys.argv[2], record))
