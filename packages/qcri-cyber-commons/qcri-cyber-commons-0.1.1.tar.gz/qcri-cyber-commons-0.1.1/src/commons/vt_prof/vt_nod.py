'''
Description: VT NOD
Author: @nabeelxy
Note:
- This represents queries made by users (may not necessarily new scans)
'''

import sys
import psycopg2
import time
import myutils
import agg_hosts
import agg_domains


def update_vt_url(vt, databasename):
    try:
        conn = psycopg2.connect(database=databasename, user="pdns", password="pdns", host = "10.4.8.61", port=5432)
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
    for host, data in vt.items():
        if host == None or len(host) == 0:
            continue
        if count % blocksize == 0:
            s_time = time.time()
            for cid in cursors:
                cursors[cid].execute("COMMIT")
                conn.commit()
                cursors[cid].execute("BEGIN")
                e_time = time.time()
                elapsed_time = e_time - s_time
                #print ("line " + str(count) + " inserts = " + str(insert_count) + " updates = " + str(update_count) + " time = " + str(elapsed_time) + '\r')
        firstseen = data['firstseen']
        lastseen = data['lastseen']
        seen_count = data['total']
        mal_count = data['mal_count']
        ts = ""
        if databasename == "vt_url_ts":
            for scan_id, result in data['scans'].items():
                if len(ts) > 0:
                    ts += '##'
                ts += scan_id + '#' +result
        elif databasename == "vt_nod":
            for host2 in data['hosts']:
                if len(ts) > 0:
                    ts += '##'
                ts += host2            

        count += 1
            
        tablename = myutils.get_table(host)
        cursor_key = myutils.get_cursor_key(host)
        try:
            cursor = cursors[cursor_key]
        except KeyError:
            print("KeyError: save to special: Domain: {}".format(host))
            cursor = cursors["special"] #TODO: get rid of hard coded keys
            
        update_stmt = None
        params = None
        try:
            update_stmt = "UPDATE " + tablename + " SET firstseen = least(firstseen, %s), lastseen = greatest(lastseen, %s), count = count + %s, mal_count = mal_count + %s, ts = ts || '##' || %s WHERE domain = %s"; 
            params = (firstseen, lastseen, seen_count, mal_count, ts, host)
        except Exception as e:
            print("ERROR: Likely a type error in the update statement")
            print(e)
            pass
            continue

        try:
            cursor.execute(update_stmt, params)
        except ValueError:
            print("ValueError: update {}".format(host))

        if (cursor.rowcount == 0):
            insertquery = None
            params1 = None
            try:
                insertquery = "INSERT INTO " + tablename + " (domain, firstseen, lastseen, count, mal_count, ts) VALUES (%s, %s, %s, %s, %s, %s);" 
                params1 =  (host, firstseen, lastseen, seen_count, mal_count, ts)
            except Exception as e:
                print("ERROR: Likely a type error in the insert statement")
                print(e)
                pass
                continue
            try:
                insert_cursors[cursor_key].execute(insertquery, params1);
            except ValueError:
                print("ValueError: insert {}".format(host))
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
    if len(sys.argv) < 3:
        print ("Usage:", sys.argv[0], "<startdate YYYYMMDD> <enddate YYYYMMDD> <databasename [vt_url_ts|vt_nod]>")
        sys.exit()
    startdate = sys.argv[1]
    enddate = sys.argv[2]
    database = sys.argv[3]

    vt = None
    if database == 'vt_url_ts':
        vt = agg_hosts.get_vt(startdate, enddate)
    elif database == 'vt_nod':
        vt = agg_domains.get_vt(startdate, enddate)
    else:
        print("ERROR: Invalid database")
        exit()

    update_vt_url(vt, database)
