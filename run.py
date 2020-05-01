import networkx as nx
import pickle
import itertools
from networkx.algorithms.boundary import node_boundary
import random
import sys
import time

eGraph = pickle.load(open('./datasets/egraphs/%s.p' %sys.argv[1],'rb'))

def similarity(i, j, eGraph):
    # edge_wt =  eGraph.get_edge_data(i,j)['weight']
    n1 = set(eGraph.neighbors(i))
    n2 = set(eGraph.neighbors(j))
    common = n1.intersection(n2)
    n1 = n1-common
    n2 = n2-common
    sum_c = 0
    for k in common:
        sum_c += sum(eGraph.get_edge_data(i, k)['weight'][m]*eGraph.get_edge_data(
            i, k)['weight'][m] for m in eGraph.get_edge_data(i, k)['weight'])
    sum_total = sum_c
    for k in n1:
        sum_total += sum(eGraph.get_edge_data(i, k)['weight'][m]*eGraph.get_edge_data(
            i, k)['weight'][m] for m in eGraph.get_edge_data(i, k)['weight'])
    for k in n2:
        sum_total += sum(eGraph.get_edge_data(j, k)['weight'][m]*eGraph.get_edge_data(
            j, k)['weight'][m] for m in eGraph.get_edge_data(j, k)['weight'])
    if sum_total == 0:
        return 0
    return (sum_c/sum_total)


def shell_nodes(eGraph, community, node, s_nodes):
    shell_nodes = s_nodes
    shell_nodes += list(set(eGraph.neighbors(node)) - set(community))
    shell_nodes.sort()
    return list(set(shell_nodes))


def lcinternal(s_node, community, eGraph, lc_int):
    internal_val = 0
    for i in community:
        internal_val += similarity(s_node, i, eGraph)
    updated_lc = ((lc_int*len(community)) + internal_val)*(len(community)+1)
    return updated_lc


def lcexternal(s_node, community, network, lc_ext, boundary_nodes,s_nodes):
    boundary_nodes = [] + add_b_nodes(shell_nodes, community)
    internal_val = 0
    for i in boundary_nodes:
        for k in s_nodes:
            internal_val += similarity(i, k, eGraph)
    updated_lc = ((lc_ext*len(boundary_nodes)) + internal_val) * \
        (len(boundary_nodes)+1)
    return updated_lc


def add_b_nodes(shell_nodes, community):
    boundary_nodes = []
    for j in community:
        nodes = []
        nodes += list(eGraph.neighbors(j))
        nodes = list(set(nodes))
        if len(set(nodes) - set(community)) > 0:
            boundary_nodes.append(j)
    return boundary_nodes

def find_community (seed) :
    community = [seed]
    boundary_nodes = [seed]
    lc_int = 1
    lc_ext = 1
    s_nodes = shell_nodes(eGraph, community, seed, [])
    for i in s_nodes[:]:
        updated_in = lcinternal(i, community, eGraph, lc_int)
        updated_ex = lcexternal(i, community, eGraph, lc_ext, boundary_nodes,s_nodes)
        if lc_int/lc_ext > updated_in / updated_ex:
            community.append(i)
            s_nodes = shell_nodes(eGraph, community, seed, s_nodes)
            lc_int = updated_in
            lc_ext = updated_ex
            s_nodes.remove(i)
            boundary_nodes.append(i)
        else:
            s_nodes.remove(i)
    return community

def all_communities ():
    start = time.time()
    all_nodes = list(eGraph.nodes)
    communities = []
    while len(all_nodes) > 0:
        community = find_community(all_nodes[0])
        communities.append(community)
        all_nodes = list(set(all_nodes) - set(community))
    # print (communities)
    end = time.time()
    print ("Time (seconds) : ", end - start)
    print ("No. of communities : ", len(communities))
    pickel_out = open("./output/%s_com.p" %sys.argv[1], 'wb')
    pickle.dump(communities, pickel_out)
    pickel_out.close()

all_communities()
