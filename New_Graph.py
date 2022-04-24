import json
import networkx as nx
import time
from pyvis.network import Network

class Graph:
    data = []
    Metabolites = [] #fill with search (needed only when creating a graph de novo
    Reaction = [] #fill with search
    nodes_metabolites = []
    nodes_reactions = []
    edges = []
    meta_keyword = [] #liste of keyword during search
    reac_keyword = [] #liste temp pour garder les catégories pour reactions et metabolites
    G = nx.MultiDiGraph()

    #open the reference file and sort the metabolic and reaction by alphabetic order of ID.
    def Load_json(self, file):
        with open(file, "r") as json_file:
            self.data = json.load(json_file)



    def __init__(self, file):
        self.Load_json(file)

    def clear_data(self):
        self.Metabolites.clear()
        self.Reaction.clear()

    def print_data(self):
        print("\nmetabolites not sorted", self.data["metabolites"])
        print("\nreaction not sorted", self.data['reactions'])

    def meta_keyword_update(self,keyword):
        self.meta_keyword.append(keyword)

    def reac_keyword_update(self,keyword):
        self.reac_keyword.append(keyword)


    def create_nodes_metabolites(self, data):
        for item in data:
            item["size"] = 20
            item["group"] = 2
            item["title"] = item["id"]
            if "name" in item:
                del item["name"]
            self.nodes_metabolites.append((item['id'], item))
        print("\nmetabolites sorted for networkX ", self.nodes_metabolites)

    def create_nodes_reactions(self, data):
        for item in data:
            item["size"] = 50
            item["group"] = 1
            item["title"] = item["id"]
            if "name" in item:
                del item["name"]
            self.nodes_reactions.append((item['id'], item))
        print("\nreaction sorted for networkX", self.nodes_reactions)

    def create_edges(self, type):
        for reaction in type:
            for metabolite, stoech in reaction["metabolites"].items():
                if stoech > 0:
                    self.edges.append([reaction["id"], metabolite])
                if stoech < 0:
                    self.edges.append([metabolite, reaction["id"]])

    #search for metabolites based on list of metabo ID
    #Does not work --> Forgot to add all the remainging metabolites.
    def search_metabolites(self):
        temp_meta = {}
        for key in self.meta_keyword:
            for item in self.data["reactions"]:
                if key in item["metabolites"] and item not in self.Reaction:
                    self.Reaction.append(item)
                    temp_meta = item["metabolites"]
            for item in self.data["metabolites"]:
                if item["id"] in temp_meta.keys() and item not in self.Metabolites:
                    self.Metabolites.append(item)
        self.meta_keyword.clear()

    #search for reactions based on list of reaction ID
    def search_reactions(self):
        temp_meta = {}
        for key in self.reac_keyword:
            for item in self.data["reactions"]:
                if item["id"] == key and item not in self.Reaction:
                    self.Reaction.append(item)
                    temp_meta = item["metabolites"]
            for item in self.data["metabolites"]:
                if item["id"] in temp_meta.keys() and item not in self.Metabolites:
                    self.Metabolites.append(item)
        self.meta_keyword.clear()
        print("Metabolites",self.Metabolites)
        print("Reactions", self.Reaction)

    # ------------------ Functions to load and save graphs ------------------- #

    def load_graph(self):
        self.create_nodes_metabolites(self.data["metabolites"])
        self.create_nodes_reactions(self.data["reactions"])
        self.create_edges(self.data["reactions"])
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

    # ------------------ Functions to show graph ----------------------------- #

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
          "edges": {
          "arrows": {
            "to": {
                "enabled": true,
                "scaleFactor": 1.4
            }
        },
            "color": {
              "inherit": true
            },
            "smooth": {
              "forceDirection": "none"
            }
          },
          "interaction": {
            "hideEdgesOnDrag": true
          },
          "physics": {
            "minVelocity": 0.75
          }
        }
        """)
        nt.show('nx.html')




