'''
Parse ADNS data collected into csv
'''
import sys
import datetime
from datetime import date, timedelta
import re

def isIp(tex):
    #if it is not match with regex it get error due to span
    try:
        return re.match('\d+\.\d+\.\d+\.\d+', tex).span()[1] == len(tex)
    except:
        return False

def get_date_obj(date_str):
    return datetime.datetime.strptime(date_str, "%Y%m%d").date()

def parser(values):
    node1=values[0]
    tableValue = [node1]

    if isIp(node1):
        print('First parameter is ip adress :' + node1)
        tableValue.append('ip')
    else:
        tableValue.append('domain')
        #domin name most of time contain '.' at the end of, remove it
        if node1.endswith('.'):
            node1 = node1[0:-1] #remove last charecter
            tableValue[0] = node1

    node2=values[-1]
    tableValue.append(node2)
    if isIp(node2):
        tableValue.append('ip')
    else:
        tableValue.append('domain')
        #domin name most of time contain '.' at the end of, remove it
        if node2.endswith('.'):
            node2 = node2[0:-1]  # remove last charecter
            tableValue[2] = node2

    #length of medium region does not known therefor first and last index except all value combined with ' '
    middleRegion = ''
    for str in values[1:-1]:
        middleRegion += str + ' '

    if 'IN A' in middleRegion:
        if 'domain' in tableValue[3]:
            print('ip type edge not domain2ip'+tableValue)
        tableValue.append('ip')
    elif 'MX' in middleRegion:
        tableValue.append('mx')
        #node2 contain mx score
        splitted = node2.split(':')
        node2=''
        for split in splitted[:-1]:
            node2 += split
        #last split removed
        if node2.endswith('.'):
            node2 = node2[0:-1]  # remove last charecter
        tableValue[2] = node2

    elif 'NS' in middleRegion:
        tableValue.append('ns')
    elif 'canonicalname' in middleRegion:
        tableValue.append('alias')
    # else:
    #     print('error unknown edge type')

    return tableValue

def parse_file(filename, outfile):
    outf = open(outfile, "w")
    with open(filename) as lines:
        for line in lines:
            values = line.split()
            if len(values) < 3:
                continue
            values = parser(values) #parse file line to database ordered data
            if len(values) != 5:
                continue

            if 'alias' in values[4]:
                #exclude cname records with same domains both sides
                if values[0] == values[2]:
                    continue
            outf.write("{}\n".format(" ".join(values)))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: parser4adns.py <adns_file> <outfile>")
        sys.exit(0)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    parse_file(input_file, output_file)
