import pickle
import networkx as nx
import sys

communities = pickle.load(open("./output/%s_com.p" % sys.argv[1], 'rb'))
eGraph = pickle.load(open("./datasets/egraphs/%s.p" % sys.argv[1], 'rb'))

all_nodes = list(eGraph.nodes)


def clustering_coeff(eGraph, communities):
    coeffs = nx.clustering(eGraph)
    avg_coeff = []
    global_avg = 0
    max = -1
    for li in communities:
        sum = 0
        total = 0
        for i in li:
            sum += coeffs[i]
            total += 1
        avg = sum/total
        if (avg > max):
            max = avg
        global_avg += avg
        avg_coeff.append((avg, total))
    global_avg = global_avg/len(communities)
    return (avg_coeff, global_avg, max)

avgerage_coeff = clustering_coeff(eGraph, communities)
print("Clustering coeff: " , avgerage_coeff[1])

def get_strength (vector):
    sum = 0
    for i in vector.keys():
        sum +=vector[i]
    return sum


def unifiablity(com1, com2):
    int_strength = 0
    ext_strength = 0
    for i in com1:
        for j in com2:
            if eGraph.has_edge(i,j):
                int_strength += get_strength(eGraph[i][j]['weight'])
    for i in com1:
        for j in list (set(all_nodes) - set(com1)):
            if eGraph.has_edge(i,j):
                ext_strength += get_strength(eGraph[i][j]['weight'])
    for i in com2:
        for j in list (set(all_nodes) - set(com2)):
            if eGraph.has_edge(i,j):
                ext_strength += get_strength(eGraph[i][j]['weight'])
    ext_strength -= int_strength
    if ext_strength <= 0:
        return 0
    return int_strength / ext_strength

def unifiablity_avg (communities):
    sum = 0
    k = 0
    for i in range(len(communities)-1):
        for j in range (i+1,len(communities)):
            sum += unifiablity (communities[i],communities[j])
            k += 1
            # print (k,sum)
        # if k % 100 == 0:
        #     print ("Iteration : ", k)
    return sum / k

uni = unifiablity_avg(communities)
print ("Unifiablity: ",uni)

def isolability (com):
    int_strength = 0
    ext_strength = 0
    for i in range(len(com)-1) :
        for j in range(i+1,len(com)) :
            if eGraph.has_edge(com[i],com[j]):
                int_strength += get_strength(eGraph[com[i]][com[j]]['weight'])
    for i in com:
        for j in list (set(all_nodes) - set(com)):
            if eGraph.has_edge(i,j):
                ext_strength += get_strength(eGraph[i][j]['weight'])
    ext_strength += int_strength
    if ext_strength == 0:
        return 0
    return int_strength / ext_strength 

def isolability_avg (communities):
    sum = 0
    for i in range(len(communities)):
        sum += isolability (communities[i])
        # if i % 100 == 0:
        #     print ("Iteration : ", i)
    return sum / len(communities)

iso = isolability_avg(communities)
print ("Isoablity: " ,iso)