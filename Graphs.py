import json
import networkx as nx
from pyvis.network import Network

def read_Json(filename):
    with open(filename, "r") as f:
        data = json.load(f)
    return data

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
    dict = {}
    for metabolite in data["metabolites"]:
        dict[metabolite["id"]]=metabolite
    for key in dict:
        del dict[key]["name"]
    return dict


def Graph_nx(nodes_r,nodes_m, edges):
    G=nx.MultiDiGraph()
    G.add_nodes_from(nodes_r,group=1,size=50, title="nodes",shape = "s")
    G.add_nodes_from(nodes_m,group=2,size=15,title="edges")
    G.add_edges_from(edges)
    return G


def Graph_pyvis(G):
    nt = Network("750px","750px")
    nt.from_nx(G)
    # nt.add_edges(edges)
    nt.show_buttons()
    nt.toggle_hide_edges_on_drag(True)
    nt.set_edge_smooth("cubicBezier")
    # nt.toggle_stabilization(False)
    nt.show('nx.html')