import pdns

print("All records related to qcri.org:")
print (pdns.pdns_domain("qcri.org"))

print("------------------------------------------------")
print("Get first seen date of qcri.org:")
print (pdns.get_first_seen_date(pdns.pdns_domain("qcri.org")))

print("------------------------------------------------")
print("Latest 10 records related to paypal.com:")
print (pdns.pdns_domain("paypal.com", None, None, None, None, 10))

print("------------------------------------------------")
print (pdns.pdns_ip("68.178.254.25"))

print("------------------------------------------------")
print (pdns.pdns_ip("68.178.254.25", None, None, "20150101 00:00"))
