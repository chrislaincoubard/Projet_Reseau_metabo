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

    #open the reference file and stores the data as attribute.
    def Load_json(self, file):
        if file != "":
            with open(file, "r") as json_file:
                self.data = json.load(json_file)

    def __init__(self, file=None):
        if file != None :
            self.Load_json(file)
        else :
            data = []

    def load_file(self, file):
        with open(file, "r") as json_file:
            self.data = json.load(json_file)


    def clear_data(self):
        self.Metabolites.clear()
        self.Reaction.clear()
        self.edges.clear()
        self.G.clear()
        self.nodes_reactions.clear()
        self.nodes_metabolites.clear()
        self.meta_keyword.clear()
        self.reac_keyword.clear()

    def print_data(self):
        print("\nmetabolites", self.Metabolites)
        print("\nreaction", self.Reaction)
        print("\nmeta_keyword", self.meta_keyword)
        print("\nreac_keyword", self.reac_keyword)

    def meta_keyword_update(self,keyword):
        if keyword not in self.meta_keyword:
            self.meta_keyword.append(keyword)

    def reac_keyword_update(self,keyword):
        if keyword not in self.reac_keyword:
            self.reac_keyword.append(keyword)


    def create_nodes_metabolites(self, data):
        for item in data:
            item["size"] = 20
            item["group"] = 2
            item["title"] = item["id"]
            if "name" in item:
                del item["name"]
            self.nodes_metabolites.append((item['id'], item))


    def create_nodes_reactions(self, data):
        for item in data:
            item["size"] = 50
            item["group"] = 1
            # self.title_reactions(data)
            item["title"] = item["gene_reaction_rule"].replace(" or ", " <br>")
            if "name" in item:
                del item["name"]
            self.nodes_reactions.append((item['id'], item))


    def create_edges(self, type):
        for reaction in type:
            for metabolite, stoech in reaction["metabolites"].items():
                if stoech > 0:
                    self.edges.append([reaction["id"], metabolite])
                if stoech < 0:
                    self.edges.append([metabolite, reaction["id"]])

    #search for metabolites based on list of metabo ID
    def search_metabolites(self):
        if not self.meta_keyword :
            return None
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
        if not self.reac_keyword:
            return None
        temp_meta = {}
        for key in self.reac_keyword:
            for item in self.data["reactions"]:
                if item["id"] == key and item not in self.Reaction:
                    self.Reaction.append(item)
                    temp_meta = item["metabolites"]
            for item in self.data["metabolites"]:
                if item["id"] in temp_meta.keys() and item not in self.Metabolites:
                    self.Metabolites.append(item)
        self.reac_keyword.clear()

    # ------------------ Functions to load and save graphs ------------------- #

    def save_graph_json(self, name):
        tot_dico = {}
        meta = []
        reac = []
        for gene in self.Reaction:
            del gene["group"]
            del gene["size"]
            del gene["title"]
        for item in self.Metabolites:
            del item["group"]
            del item["size"]
            del item["title"]
            meta.append(item)
        for item in self.Reaction:
            reac.append(item)
        tot_dico["metabolites"] = meta
        tot_dico["reactions"] = reac
        with open(name, 'w') as f:
            f.write(json.dumps(tot_dico))

    # ------------------ Functions to show graph ----------------------------- #

    def create_Graph(self,name):
        # create or show graph depending if a search has been made
        if self.meta_keyword or self.reac_keyword :
            self.search_metabolites()
            self.search_reactions()
            self.create_nodes_metabolites(self.Metabolites)
            self.create_nodes_reactions(self.Reaction)
            self.create_edges(self.Reaction)
            self.G.add_nodes_from(self.nodes_metabolites)
            self.G.add_nodes_from(self.nodes_reactions)
            self.G.add_edges_from(self.edges)
            if "html" in name:
                self.show_graph(name)
            else :
                self.show_graph(name+".html")
        else :
            self.create_nodes_metabolites(self.data["metabolites"])
            self.create_nodes_reactions(self.data["reactions"])
            self.create_edges(self.data["reactions"])
            self.G.add_nodes_from(self.nodes_metabolites)
            self.G.add_nodes_from(self.nodes_reactions)
            self.G.add_edges_from(self.edges)
            if "html" in name :
                self.show_graph(name)
            else :
                self.show_graph(name+".html")


    def show_graph(self, name):
        nt = Network("1000px", "1000px")
        nt.from_nx(self.G)
        # nt.show_buttons() # show buttons must be turned off if non-default paramaters are set
        nt.toggle_hide_edges_on_drag(True)
        nt.set_edge_smooth("dynamic")

        nt.set_options("""
        var options = {
        "nodes": {
            "borderWidthSelected": 5
           },
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
        nt.show(name)




