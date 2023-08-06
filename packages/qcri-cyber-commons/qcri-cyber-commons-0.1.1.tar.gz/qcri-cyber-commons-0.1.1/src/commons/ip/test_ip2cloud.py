import ip2cloud
import sys

i2c = ip2cloud.IP2Cloud("cloud_ips.txt")

ipf = open(sys.argv[1])
outf = open(sys.argv[2], "w+")
for ip in ipf:
    ip = ip.strip().strip("\r\n")
    cloud = i2c.get(ip)
    if cloud == None:
        cloud = "none"
    outf.write("{},{}\n".format(ip, cloud))
outf.close()

