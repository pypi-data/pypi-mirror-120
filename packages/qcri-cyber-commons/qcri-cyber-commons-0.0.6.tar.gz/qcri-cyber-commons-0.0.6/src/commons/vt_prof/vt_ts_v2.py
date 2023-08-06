'''
Description: VT TS - create a summary of VT records. Considers all URLs
Author: @nabeelxy
Note:
- This represents queries made by users (may not necessarily new scans)
'''

import sys
import os
import psycopg2
import time
import myutils
from datetime import timedelta, datetime
import fnmatch
#v3
#from urllib.parse import urlparse
#v27
from urlparse import urlparse

BASE_VT_DIR = "/export/sec04/vt/vt_url_feed_parsed_v2"


def append_files(startdate, enddate):                        
    s_date = datetime.strptime(startdate.strip(), "%Y%m%d").date()
    e_date = datetime.strptime(enddate.strip(), "%Y%m%d").date() 
    delta = e_date - s_date                                                       
    for i in range(delta.days + 1):                                               
        curr_date = s_date + timedelta(i)                                           
        name = "res.url-feed-{}T??".format(curr_date.strftime("%Y%m%d"))
        filenames = fnmatch.filter(os.listdir(BASE_VT_DIR), name)
        for filename in filenames:
            full_path = os.path.join(BASE_VT_DIR, filename)
            print("Inserting {}".format(filename))
            update(full_path, "vt_ts_v2")

def update(filename, databasename):
    try:
        conn = psycopg2.connect(database=databasename, user="pdns", password="pdns", host = "127.0.0.1", port=5432)
        print("Connected")
    except:
        print ("I am unable to connect to the database")
        return

    cursors = dict()
    insert_cursors = dict()

    prefixes = myutils.get_prefixes_new()
    for prefix in prefixes:
        cursors[prefix] = conn.cursor()
        insert_cursors[prefix] = conn.cursor()

    #print cursors
    count = 0
    insert_count = 0
    update_count = 0
    duplicate_count = 0
    nulldomain = 0
    nullip = 0
    emptydomain = 0
    emptyip = 0
    start_time = time.time()
    for cid in cursors:
        cursors[cid].execute("BEGIN")

    for cid in insert_cursors:
        insert_cursors[cid].execute("BEGIN")

    blocksize = 100000
    fn = open(filename)
    for line in fn:
        values = line.split("##")
        if (len(values) != 5):
            print ("Invalid format {0}\n".format(line))
            continue

        url = values[0]
        if url == None or len(url) == 0:
            print("ERROR: Invalid URL: {}".format(line))
            continue

        try:
            uri = urlparse(url)
        except Exception as e:
            print("ERROR: Something went wrong when parsing the url: {}".format(url))
            print(e)
            pass
            continue

        domain = uri.netloc
        path_len = len(uri.path.strip('/'))
        query_len = len(uri.query)

        if domain == None or len(domain) == 0:
            print("WARNING: empty domain: {}".format(line))
            continue

        datestr = values[1]
        epoch = None

        #conservatively exclude format errors
        try:
            epoch = int(datetime.strptime(datestr, '%Y-%m-%d %H:%M:%S').strftime('%s'))
        except Exception as e:
            print("ERRROR - likely format issue: {}".format(line))
            print(e)
            pass
            continue

        ts = "{} {} {} {}".format(epoch, values[3], path_len, query_len)

        if count % blocksize == 0:
            s_time = time.time()
            for cid in cursors:
                cursors[cid].execute("COMMIT")
                conn.commit()
                cursors[cid].execute("BEGIN")
            e_time = time.time()
            elapsed_time = e_time - s_time
            print ("line " + str(count) + " inserts = " + str(insert_count) + " updates = " + str(update_count) + " time = " + str(elapsed_time) + '\r')
        firstseen = epoch
        lastseen = epoch
        seen_count = 1
        count += 1
        mal_count = 0
        if values[3] > 0:
            mal_count = 1
            
        tablename = myutils.get_table(domain)
        cursor_key = myutils.get_cursor_key(domain)
        try:
            cursor = cursors[cursor_key]
        except KeyError:
            print("KeyError: save to special: Domain: {}".format(domain))
            cursor = cursors["special"] #TODO: get rid of hard coded keys

        update_stmt = None
        params = None
        try:
            update_stmt = "UPDATE " + tablename + " SET firstseen = least(firstseen, %s), lastseen = greatest(lastseen, %s), count = count + %s, mal_count = mal_count + %s, ts = ts || '##' || %s WHERE domain = %s"; 
            params = (firstseen, lastseen, seen_count, mal_count, ts, domain)
        except Exception as e:
            print("ERROR: Likely a type error in the update statement")
            print(e)
            pass
            continue

        try:
            cursor.execute(update_stmt, params)
        except ValueError:
            print("ValueError: update {}".format(domain))
        if (cursor.rowcount == 0):
            insertquery = None
            params1 = None
            try:
                insertquery = "INSERT INTO " + tablename + " (domain, firstseen, lastseen, count, mal_count, ts) VALUES (%s, %s, %s, %s, %s, %s);" 
                params1 =  (domain, firstseen, lastseen, seen_count, mal_count, ts)
            except Exception as e:
                print("ERROR: Likely a type error in the insert statement")
                print(e)
                pass
                continue
            try:
                insert_cursors[cursor_key].execute(insertquery, params1);
            except ValueError:
                print("ValueError: insert {}".format(domain))
            insert_count += 1
        else:
            update_count += 1
    s_time = time.time()
    for cid in cursors:
        cursors[cid].execute("COMMIT")
        conn.commit()
        cursors[cid].close()
    e_time = time.time()
    elapsed_time = e_time - s_time
    print ("final update time = " + str(elapsed_time) + "\r")

    #commit inserts only at the end
    s_time = time.time()
    for cid in insert_cursors:
        insert_cursors[cid].execute("COMMIT")
        conn.commit()
        insert_cursors[cid].close()
    e_time = time.time()
    elapsed_time = e_time - s_time
    print ("final insert time = " + str(elapsed_time) + "\r")

    conn.close()

    if count != 0:
        print ("total {0} insert {1} update {2} duplicate {3}\n".format(count, insert_count, update_count, duplicate_count))
        print ("null domain {0} | empty domain {1} | null ip {2} | empty ip {3}\n".format(nulldomain, emptydomain, nullip, emptyip))
        print ("records use {0}: {1} seconds, average time per record {2} seconds.\n".format(count, time.time() - start_time, (time.time() - start_time) / count))
    else:
        print ("zero record inserted\n")

if __name__=="__main__":
    if len(sys.argv) < 2:
        print ("Usage:", sys.argv[0], "<startdate YYYYMMDD> <enddate YYYYMMDD>")
        sys.exit()
    startdate = sys.argv[1]
    enddate = sys.argv[2]
    append_files(startdate, enddate)
