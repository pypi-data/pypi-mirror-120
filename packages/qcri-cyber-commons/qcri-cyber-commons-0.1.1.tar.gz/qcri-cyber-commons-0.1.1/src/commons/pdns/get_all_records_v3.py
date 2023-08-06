import pdns
import sys


def save_all(resource, fh, limit, server_ip, resource_type):
    entries = list()
    if resource_type == "domain":
        entries = pdns.pdns_domain(resource, None, None, None, None, limit, "A", server_ip)
        print(entries)
    elif resource_type == "ip":
        entries = pdns.pdns_ip(resource, None, None, None, None, limit, server_ip)

    if entries != None:
        for entry in entries:
            fh.write("{}\n".format(entry))

def all_resources(resourcef, outfile, limit, collected, server_ip, resource_type):
    done = set()
    with open(collected) as c:
        for d in c:
            done.add(d.strip())

    fh = open(outfile, "w", 512)
    df = open(resourcef)
    for resource in df:
        try:
            if resource_type == "domain" or resource_type == "ns":
                resource = resource.strip().strip(".").encode("idna").decode()
            else:
                resource = resource.strip()
            if resource in done:
                continue
            save_all(resource, fh, limit, server_ip, resource_type)
        except Exception as e:
            pass
    fh.close()

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Usage: resource_file output_file limit collected_file server_ip resource_type (domain|ip|ns)")
        exit()

    resourcefile = sys.argv[1]
    outfile = sys.argv[2]
    limit = int(sys.argv[3])
    collected = sys.argv[4]
    server_ip = sys.argv[5]
    resource_type = sys.argv[6] #domain|ip|ns

    if resource_type not in {"domain", "ip", "ns"}:
        print("Invalid resource type: {}".format(resource_type))
        exit()

    all_resources(resourcefile, outfile, limit, collected, server_ip, resource_type)

    
