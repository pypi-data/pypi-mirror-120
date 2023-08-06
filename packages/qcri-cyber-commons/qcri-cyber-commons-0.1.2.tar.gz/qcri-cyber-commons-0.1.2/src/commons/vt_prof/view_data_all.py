import sys
import psycopg2
import myutils
import string

def get_count(cur, sequence):
  tot_rows = 0
  for char in sequence:
    letter_rows = 0
    for char2 in sequence:
      stmt = "SELECT count(*) FROM " + myutils.get_table(char + char2)
      cur.execute(stmt)
      row = cur.fetchone()
      row_count = int(row[0])
      print (stmt, " ", row_count)
      letter_rows += row_count
      
    stmt = "SELECT count(*) FROM " + myutils.get_table(char + "*")
    cur.execute(stmt)
    row = cur.fetchone()
    row_count = int(row[0])
    letter_rows += row_count
    print (stmt, " ", row_count)
    print ('Number of rows in {0} = {1}'.format(char, letter_rows))
    tot_rows += letter_rows
  return tot_rows

def count_rows(databasename):
  try:
    tot_rows = 0
    conn = psycopg2.connect(database=databasename, user="pdns", password="pdns", host="10.4.8.61", port=5432)
    cur = conn.cursor()
    tot_rows += get_count(cur, string.ascii_lowercase)
    tot_rows += get_count(cur, string.digits)
    stmt = "SELECT count(*) FROM " + myutils.get_table("*")
    cur.execute(stmt)
    row = cur.fetchone()
    row_count = int(row[0])
    tot_rows += row_count
    print ('Number of rows in {0} = {1}'.format("*", row_count))
    cur.close()
    print ('Total rows = {0}'.format(tot_rows))
  except Exception as e:
    print (e)
    print ("some error related to db occurred")
  finally:
    if conn is not None:
      conn.close()

if __name__=="__main__":
  if len(sys.argv) < 2:
    print("Usage: {} <database".format(sys.argv[0]))
    exit()
  database = sys.argv[1]
  count_rows(database)
