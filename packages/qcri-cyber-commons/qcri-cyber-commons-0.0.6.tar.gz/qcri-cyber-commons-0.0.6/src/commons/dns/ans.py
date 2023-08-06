#Obtaining the authoritative name server
import dns.resolver
import re

domain = 'co.uk'

response = dns.resolver.query(domain, 'SOA')

if response.rrset is not None:
    pattern= r'(%s)\.\s(\d{1,})\s(\w+)\sSOA\s(.*?)\.\s(.*?)\.\s(\d{1,})\s(\d{1,})\s(\d{1,})\s(\d{1,})\s(\d{1,})' % domain
    match = re.match(pattern, str(response.rrset))
    m_name, ttl, class_, ns, email, serial, refresh, retry, expiry, minim = match.groups()

output ='''
Main Name In Zone: {a},
Cache TTL: {b},
Class: {c},
Authoritive NS: {d},
Email Address: {e},
Last Change: {f},
Retry In Secs: {g},
Expiry: {h},
Slave Cache In Sec: {i}
'''.format(a = m_name, b = ttl, c = class_, d = ns, e = str(email).replace('\\', ''), f = serial, g = retry, h = expiry, i = minim)

print output

response = dns.resolver.query(domain, 'SOA')
print response.rrset
