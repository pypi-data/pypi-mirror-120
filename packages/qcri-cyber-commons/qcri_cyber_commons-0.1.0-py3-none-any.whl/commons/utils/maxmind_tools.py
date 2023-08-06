from pygeoip import GeoIP, MEMORY_CACHE

class MyGeo:
    def __init__(self, maxmind_city_file):
        self.gi = GeoIP(maxmind_city_file, MEMORY_CACHE)

    def getCountry(self, ip):
        ret = self.gi.record_by_addr(ip)
        if ret != None:
            return ret["country_name"]
        return None

    def getLatLon(self, ip):
        ret = self.gi.record_by_addr(ip)
        if ret != None:
            return [ret["latitude"], ret["longitude"]]
        return None

class MyASN:
    def __init__(self, asn_file):
        self.gi = GeoIP(asn_file, MEMORY_CACHE)

    def getasn(self, ip):
        as_str = self.gi.org_by_addr(ip)
        if as_str != None:
            arr = as_str.split()
            if len(arr) > 0:
                return arr[0].strip()
        return as_str

    def getorg(self, ip):
        as_str = self.gi.org_by_addr(ip)
        if as_str != None:
            i = as_str.find(' ')
            if i != -1:
                return as_str[i+1:].strip()

    def getasn_dom(self, domain):
        as_str = self.gi.asn_by_name(domain)
        return as_str
