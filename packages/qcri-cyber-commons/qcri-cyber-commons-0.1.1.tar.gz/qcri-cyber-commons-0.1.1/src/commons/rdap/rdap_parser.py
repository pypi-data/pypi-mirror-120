'''
Parse RDAP output to CSV format
'''
import sys

def parse_domain_whois(inputf, outputf, fields):
    inf = open(inputf)
    outf = open(outputf, "w")
    for line in inf:
        line = line.strip()

    outf.close()


def parse_ip_whois(inputf, outputf, fields):
    inf = open(inputf)
    outf = open(outputf, "w")
    


def parse_as(inputf, outputf, fields):
    inf = open(inputf)
    outf = open(outputf, "w")


