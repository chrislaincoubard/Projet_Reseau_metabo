import json
import networkx as nx
import time
from pyvis.network import Network

class Graph:
    nodes_metabolites = []
    nodes_reactions = []
    edges = []
    data = {}
    G = nx.MultiDiGraph()

    def load_json(self, file):
        with open(file, "r") as f:
            self.data = json.load(f)

    def __init__(self, file):
        self.load_json(file)

    def print_data(self):
        print(self.data)

    def create_nodes_metabolites(self):
        for item in self.data["metabolites"]:
            item["size"] = 20
            item["group"] = 2
            item["title"] = item["id"]
            if "name" in item:
                del item["name"]
            self.nodes_metabolites.append((item['id'], item))

    def create_nodes_reactions(self):
        for item in self.data["reactions"]:
            item["size"] = 50
            item["group"] = 1
            item["title"] = item["id"]
            if "name" in item:
                del item["name"]
            self.nodes_reactions.append((item['id'], item))

    def create_edges(self):
        for reaction in self.data["reactions"]:
            for metabolite, stoech in reaction["metabolites"].items():
                if stoech > 0:
                    self.edges.append([reaction["id"], metabolite])
                if stoech < 0:
                    self.edges.append([metabolite, reaction["id"]])

    def create_Graph(self):
        self.G.add_nodes_from(self.nodes_metabolites)
        self.G.add_nodes_from(self.nodes_reactions)
        self.G.add_edges_from(self.edges)

    def show_graph(self):
        nt = Network("750px", "750px")
        nt.from_nx(self.G)
        # nt.show_buttons() show buttons must be turned off if non-default paramaters are set
        nt.toggle_hide_edges_on_drag(True)
        nt.set_edge_smooth("dynamic")
        nt.set_options("""
        var options = {
          "nodes": {
            "borderWidthSelected": 5
          },
          "edges": {
            "color": {
              "inherit": true
            },
            "smooth": {
              "type": "straightCross",
              "forceDirection": "none"
            }
          },
          "interaction": {
            "hideEdgesOnDrag": true,
            "hover": true,
            "multiselect": true
          },
          "physics": {
            "barnesHut": {
              "springLength": 175,
              "avoidOverlap": 1
            },
            "minVelocity": 0.75
          }
        }
        """)
        nt.show('nx.html')


    def add_nodes_from(self, nodes):
        self.G.add_nodes_from(nodes)

    def add_edges_from(self, edges):
        self.G.add_edges_from(edges)

    def load_graph(self):
        self.create_nodes_metabolites()
        self.create_nodes_reactions()
        self.create_edges()
        self.create_Graph()
        self.show_graph()

    def save_graph_json(self, name):  # not working properly still
        tot_dico = {}
        meta = []
        reac = []
        for item in self.nodes_metabolites:
            print(self.nodes_metabolites)
            meta.append(item[1])
        for item in self.nodes_reactions:
            reac.append(item[1])
        print(meta)
        tot_dico["metabolites"] = meta
        tot_dico["reactions"] = reac
        with open(name, 'w') as f:
            f.write(json.dumps(tot_dico))

if __name__ == '__main__':
    Gr = Graph("Test_with_POO.json")
    Gr.load_graph()
    # Gr.save_graph_json("Test_with_POO.json")

