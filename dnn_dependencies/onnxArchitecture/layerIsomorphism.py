import networkx as nx
from pprint import pprint as print

G = nx.read_gexf('architecture.gexf')

H = nx.read_gexf('architecture.gexf')

#choose source nodes
sources = ["0"]

#breadth first search traversal for each graph to get layers as a dictionary (key value pairs)
layersG = {}
for layer, nodes in enumerate(nx.bfs_layers(G, sources)):
    for node in nodes:
        layersG[node] = layer

layersH = {}
for layer, nodes in enumerate(nx.bfs_layers(H, sources)):
    for node in nodes:
        layersH[node] = layer

# Check if the layers match
isomorphic = layersG == layersH

# Prints the result
if isomorphic:
    print("True")
else:
    print("False")





