import networkx as nx
import pickle
import itertools
from networkx.algorithms.boundary import node_boundary
import random
import time
import sys


network = pickle.load(open("./dataset/reality-mining/reality.pickle", "rb"))


def total_nodes (network):
    nodes = set()
    for i in network.keys():
        nodes = nodes.union(set(list(network[i].nodes)))
    return list(nodes)


def shell_nodes(network, community, node, s_nodes):
    shell_nodes = s_nodes
    for i in network.keys():
        if network[i].has_node(node):
            shell_nodes += list(set(network[i].neighbors(node)
                                    ) - set(community))
    return list(set(shell_nodes))


def lcinternal(s_node, community, network, lc_int):
    internal_val = 0
    for i in community:
        for j in network.keys():
            if network[j].has_node(s_node) and network[j].has_node(i):
                internal_val += list(nx.jaccard_coefficient(
                    network[j], [(s_node, i)]))[0][2]
    updated_lc = ((lc_int*len(community)) + internal_val)*(len(community)+1)
    return updated_lc


def add_b_nodes(shell_nodes, community):
    boundary_nodes = []
    for j in community:
        nodes = []
        for i in network.keys():
            if network[i].has_node(j):
                nodes += list(network[i].neighbors(j))
        nodes = list(set(nodes))
        if len(set(nodes) - set(community)) > 0:
            boundary_nodes.append(j)
    return boundary_nodes


def lcexternal(s_node, community, network, lc_ext, boundary_nodes,s_nodes):
    boundary_nodes = [] + add_b_nodes(shell_nodes, community)
    internal_val = 0
    for i in boundary_nodes:
        for j in network.keys():
            if network[j].has_node(i):
                for k in s_nodes:
                    if network[j].has_node(k):
                        internal_val += list(nx.jaccard_coefficient(
                            network[j], [(i, k)]))[0][2]
    updated_lc = ((lc_ext*len(boundary_nodes)) + internal_val) * \
        (len(boundary_nodes)+1)
    return updated_lc


def find_community(seed):
    community = [seed]
    boundary_nodes = [seed]
    lc_ext = 1
    lc_int = 1
    s_nodes = shell_nodes(network, community, seed, [])
    for i in s_nodes[:]:
        updated_in = lcinternal(i, community, network, lc_int)
        updated_ex = lcexternal(i, community, network, lc_ext, boundary_nodes,s_nodes)
        if lc_int/lc_ext > updated_in / updated_ex:
            community.append(i)
            s_nodes = shell_nodes(network, community, seed, s_nodes)
            lc_int = updated_in
            lc_ext = updated_ex
            s_nodes.remove(i)
            boundary_nodes.append(i)
        else:
            s_nodes.remove(i)
    return community


def all_communities ():
    start = time.time()
    all_nodes = total_nodes(network)
    communities = []
    while len(all_nodes) > 0:
        community = find_community(all_nodes[0])
        communities.append(community)
        all_nodes = list(set(all_nodes) - set(community))
    # print (communities)
    end = time.time()
    print ("Time (seconds) : ", end - start)
    print ("No. of communities : ", len(communities))
    pickel_out = open("./result/%s_com_old.pickle" %sys.argv[1], 'wb')
    pickle.dump(communities, pickel_out)
    pickel_out.close()

all_communities()
