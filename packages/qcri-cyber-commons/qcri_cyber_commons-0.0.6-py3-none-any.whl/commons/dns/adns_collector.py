'''
Description: Collect active DNS records related data for domains
'''
import dns.resolver
import sys
from multiprocessing import Pool

#given a domain, get the DNS records
def get_dns_resolution(domain):
  records = list()
  try:
    answer = dns.resolver.query(domain)
    records.append(answer.rrset)
    records.append("{}. canonicalname {}".format(domain, answer.canonical_name))
    records.append("{}. qname {}".format(domain, answer.qname))
    records.append("{}. expiration {}".format(domain, answer.expiration))
    records.append("{}. rdclass {}".format(domain, answer.rdclass))
    records.append("{}. rdtype {}".format(domain, answer.rdtype))
    try:    
      mxrecords = dns.resolver.query(domain, 'MX')
      for rdata in mxrecords:
        records.append("{}. MX {}:{}".format(domain, rdata.exchange, rdata.preference))
    except dns.resolver.NoAnswer:
      pass #ignore ones without MX records
    try:
      nsrecords = dns.resolver.query(domain, 'NS')
      for rdata in mxrecords:
        records.append("{}. NS {}".format(domain, rdata))
    except:
      pass #ignore ones without NS records
  except dns.resolver.NXDOMAIN as e:
    answer = "##NXDOMAIN##"
    records.append("{}. {}".format(domain, answer))
  except dns.resolver.Timeout:
    answer = "##TIMEOUT##"
    records.append("{}. {}".format(domain, answer))
  except Exception as e:
    answer = "##ERRORR##"
    records.append("{}. {}".format(domain, answer))
    print(e)
  return records

#Get DNS detaisl for a list of domains in a text file and write the output back
#to a file
def get_dns_resolutions_file(in_put):
    records = get_dns_resolution(in_put)
    return records


#run the program
if __name__ == '__main__':
    inputf  = open(sys.argv[1].strip(),'r', encoding = 'utf-8')
    outputf = open(sys.argv[2].strip(),'w+', encoding = 'utf-8')
    #use 30 cores
    workers = Pool(30)
    #parallel workload -asynchronous
    records = workers.map(get_dns_resolutions_file, [x.split('\n')[0] for x in inputf.readlines()])
    #write on file - synchronous
    for result in records:
        for record in result:
            outputf.write(str(record)+'\n')
        
    inputf.close()
    outputf.close()    
