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

    def title_reactions(self,data):
        for gene in data:
            gene["gene_reaction_rule"] = gene["gene_reaction_rule"].replace(" or ", " <br> ")

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
            # self.title_reactions(data)
            item["title"] = item["gene_reaction_rule"].replace(" or ", " <br>")
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
        self.reac_keyword.clear()

    # ------------------ Functions to load and save graphs ------------------- #

    def load_graph(self):
        self.create_nodes_metabolites(self.data["metabolites"])
        self.create_nodes_reactions(self.data["reactions"])
        self.create_edges(self.data["reactions"])
        self.create_Graph()
        self.show_graph("My_graph.html")

    def save_graph_json(self, name):  # not working properly still
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

    def create_Graph(self):
        self.G.add_nodes_from(self.nodes_metabolites)
        self.G.add_nodes_from(self.nodes_reactions)
        self.G.add_edges_from(self.edges)

    def show_graph(self, name):
        nt = Network("1000px", "1000px")
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



if __name__ == '__main__':

    g = Graph("test_BR.json")
    # g.meta_keyword_update("ADP_c")
    # g.meta_keyword_update("CPD-8843_c")
    # g.meta_keyword_update("GTP_c")
    # g.search_metabolites()
    # g.create_nodes_metabolites(g.Metabolites)
    # g.create_nodes_reactions(g.Reaction)
    # g.create_edges(g.Reaction)
    # g.create_Graph()
    # g.show_graph("My_graph.html")
    # g.save_graph_json("test_BR.json")
    g.load_graph()

