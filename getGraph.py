import networkx as nx
import pickle as pk
import sys

dataset = sys.argv[1]
file = open("./datasets/{}.txt".format(dataset),"r")

graph = nx.Graph()
num_layers = 5
edges = []
for i in file.readlines():
    l = i.split()
    edges.append((int(l[0]),int(l[1])))

for i in edges:
    graph.add_edge(*i,weight = {})


layers=[edges[i:i + int(len(edges)/num_layers)] for i in range(0, len(edges), int(len(edges)/num_layers))]

for i in range(len(layers)):
    for j in layers[i]:
        if graph.has_edge(*j):
            newweight = graph.get_edge_data(*j)['weight']
            newweight[i] = 1
            graph.add_edge(*j, weight=newweight)
        else:
            graph.add_edge(*j,weight = {i:1})

# print (graph.number_of_nodes())

graph_copy = graph

edge_list = graph.edges()
for j in edge_list:
    edge_data = graph.get_edge_data(*j)['weight']
    updated_data = {}
    for i in edge_data.keys():
        if i==0 and i+1<=num_layers:
            updated_data[i] = edge_data[i]/2
            if i+1 in edge_data.keys():
                updated_data[i+1] = edge_data[i]/2  + edge_data[i+1]
            else:
                updated_data[i+1] = edge_data[i]/2
        elif i==num_layers and i-1>=0:
            updated_data[i] = edge_data[i]/2
            if i-1 in edge_data.keys():
                updated_data[i-1] = edge_data[i]/2  + edge_data[i-1]
            else:
                updated_data[i-1] = edge_data[i]/2
        else:
            updated_data[i] = edge_data[i]/3
            if i+1 in edge_data.keys():
                updated_data[i+1] = edge_data[i]/3  + edge_data[i+1]
            else:
                updated_data[i+1] = edge_data[i]/3
            if i-1 in edge_data.keys():
                updated_data[i-1] = edge_data[i]/3  + edge_data[i-1]
            else:
                updated_data[i-1] = edge_data[i]/3
    graph.add_edge(*j,weight = updated_data)
    # print (graph.get_edge_data(*j))

pk.dump(graph, open("./datasets/egraphs/{}.p".format(dataset),"wb"))
print ("Created e-graph.")