'''
Description: Given an IP address, it finds the cloud hosting provider (if any). 
Currently, we support aws, gce and azure.
Author: nabeelxy
'''
import ipaddress

class IP2Cloud:
    #filelist - a csv file of the format <cloud>,<filepath>
    def __init__(self, filelist):
        file_dict = dict()
        fh = open(filelist)
        for line in fh:
            arr = line.split(",")
            if len(arr) != 2:
                raise ValueError("ERROR: invalid format: {}".format(line))
            cloud = arr[0].strip()
            filename = arr[1].strip()
            file_dict[cloud] = filename
        self.clouds = dict()
        for cloud in file_dict:
            self.clouds[cloud] = self.load_subnets(file_dict[cloud])

    def load_subnets(self, inputfile):
        ipf = open(inputfile)
        subnets = dict()
        for subnet in ipf:
            subnet = subnet.strip()
            n = ipaddress.ip_network(subnet)
            subnets[subnet] = [int(n.network_address), int(n.netmask)]        
        return subnets

    def in_network(self, address, network, mask):
        addr = int(ipaddress.ip_address(address))
        return (addr & mask) == network

    def get(self, address):
        for cloud in self.clouds:
            for subnetname in self.clouds[cloud]:
                subnet = self.clouds[cloud][subnetname]
                if self.in_network(address, subnet[0], subnet[1]):
                    return cloud
        return None
    
        
