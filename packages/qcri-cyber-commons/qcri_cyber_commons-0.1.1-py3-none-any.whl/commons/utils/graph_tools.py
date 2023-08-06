# Creating graphs and visualizing

#[g, edges, domains, ips] = create_graph("edges.csv")
#draw_domain_ip_graph(g, edges, domains, ips, mal_domains)

import networkx as nx
import matplotlib.pyplot as plt

def create_graph(edge_file):
    ef = open(edge_file)
    g = nx.Graph()
    edge_list = list()
    domains = set()
    ips = set()
    for line in ef:
        arr = line.strip().split()
        g.add_edge(arr[0], arr[1])
        domains.add(arr[0])
        ips.add(arr[1])
        edge_list.append((arr[0], arr[1]))
    return [g, edge_list, list(domains), list(ips)]

def draw_domain_ip_graph(g, edges, node_lists, labeling = 1, gw = 20, gh = 10, k = 0.15, itr = 20):
    plt.figure(figsize=(20,10))
    pos = nx.spring_layout(g,k=0.15,iterations=20)
    for node_list in node_lists:
        nodes = node_list[0]
        color = node_list[1]
        nx.draw_networkx_nodes(g, pos, nodelist = nodes, node_color = color)
    #nx.draw_networkx_nodes(g, pos, nodelist = domains, node_color = 'blue')
    #nx.draw_networkx_nodes(g, pos, nodelist = ips, node_color = 'green')
    #nx.draw_networkx_nodes(g, pos, nodelist = mal_domains, node_color = 'red')
    nx.draw_networkx_edges(g, pos, edge_list = edges, width = 2, edge_color = 'black')
    
    if labeling == 1:
        labels = dict()
        for node in g.nodes:
            labels[node] = node
        #for domain in domains:
        #    labels[domain] = domain
        #for ip in ips:
        #    labels[ip] = ip
        nx.draw_networkx_labels(g, pos, labels, font_size = 12)

def get_edge_set(all_edges, cc, outfile):
    edges = set()
    outf = open(outfile, "w")
    for edge in all_edges:
        if edge[0] == edge[1]:
            continue
        if edge[0] in cc:
            edges.add(edge)
    for edge in edges:
        outf.write("{} {}\n".format(edge[0], edge[1]))
    outf.close()
    return edges

def get_cc_sizes(g):
    return [len(c) for c in sorted(nx.connected_components(g), key=len, reverse=True)]

def get_cc_nodes(g):
    cc_nodes = []
    for cc in nx.connected_components(g):
        cc_nodes.append(g.subgraph(cc).copy().nodes)
