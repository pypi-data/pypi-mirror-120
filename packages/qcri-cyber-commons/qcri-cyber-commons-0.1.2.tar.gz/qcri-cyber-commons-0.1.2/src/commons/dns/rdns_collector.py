'''
Description: Collect reverse DNS records related data for IPs
'''
import sys
from multiprocessing import Pool
import socket

#given an IP, get the PTR record
def get_rdns(ip):
  records = list()
  try:
    answer = socket.gethostbyaddr(ip)
    if len(answer) > 1:
        records.append("{} {}".format(ip, answer[0]))
  except socket.herror as e:
    answer = "##UNKNOWNHOST##"
    records.append("{} {}".format(ip, answer))
  except Exception as e:
    answer = "##ERRORR##"
    records.append("{} {}".format(ip, answer))
    print(e)
  return records

#Get DNS detaisl for a list of domains in a text file and write the output back
#to a file
def get_rdns_file(in_put):
    records = get_rdns(in_put)
    return records


#run the program
if __name__ == '__main__':
    inputf  = open(sys.argv[1].strip(),'r')
    outputf = open(sys.argv[2].strip(),'w+')
    #use 30 cores
    workers = Pool(30)
    #parallel workload -asynchronous
    records = workers.map(get_rdns_file, [x.split('\n')[0] for x in inputf.readlines()])
    #write on file - synchronous
    for result in records:
        for record in result:
            outputf.write(str(record)+'\n')
        
    inputf.close()
    outputf.close()    
