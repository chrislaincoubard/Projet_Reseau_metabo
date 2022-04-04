import json
import networkx as nx
import time
from pyvis.network import Network

# from networkx.drawing.nx_pydot import write_dot
# import matplotlib.pyplot as plt
# from graphviz import Source

with open("Test_glycolysis.json", "r") as f:
    data = json.load(f)

def create_edges(data):
    edges = []
    for reaction in data["reaction"]:
        for metabolite, stoech in reaction["metabolites"].items():
            if stoech > 0:
                edges.append([reaction["id"],metabolite])
            if stoech < 0:
                edges.append([metabolite,reaction["id"]])
    return tuple(edges)


def create_nodes_metabolites(data):
    nodes = []
    for metabolite in data["metabolites"]:
        nodes.append(metabolite["id"])
    return nodes

def create_nodes_reactions(data):
    nodes = []
    for reaction in data["reaction"]:
        nodes.append(reaction["id"])
    return nodes

def nodes_attributes(data):
    dict ={}
    for metabolite in data["metabolites"]:
        dict[metabolite["id"]]=metabolite
    for key in dict:
        del dict[key]["name"]
    return dict

def add_nodes_with_size(data,taille,groupe,Graph):
    for node in data:
        Graph.add_node(node, size=taille, group=groupe)


def GraphLOL(nodes_r,nodes_m, edges):
    """ Visualize a directed multigraph as a dot file """
    G=nx.MultiDiGraph()
    # add_nodes_with_size(nodes_r,10,2,G)
    # add_nodes_with_size(nodes_m,5,1,G)
    G.add_nodes_from(nodes_r,group=1,size=50)
    G.add_nodes_from(nodes_m,group=2,size=20)
    G.add_edges_from(edges)
    nx.set_node_attributes(G,dict)
    nt = Network("750px","750px")
    nt.from_nx(G)
    nt.add_edges(edges)
    nt.show_buttons(filter_=['nodes','physics'])
    nt.toggle_hide_edges_on_drag(True)
    nt.set_edge_smooth("straightCross")
    nt.show('nx.html')


start_time = time.time()
nodes_m = create_nodes_metabolites(data)
nodes_r = create_nodes_reactions(data)
edges = create_edges(data)
dict = nodes_attributes(data)


GraphLOL(nodes_r,nodes_m,edges)
print("---- %s s -----" % (time.time()-start_time))
# piece of code (a bit dirty) to get the value of all attribute of nodes of a graph
# for node in G:
#     for attribute in G.nodes[node]:
#         print(f"node : {node} attribute : {attribute} as a value of {G.nodes[node][attribute]}")
