import json
import networkx as nx
import time
from pyvis.network import Network


#     print("Type:", type(data))
#     print(type(data['metabolites']))
#     print("\nmetabolites:", data['metabolites'])
#     print("\nmetabolites:", sorted(data['metabolites'], key=lambda k: k['name']))
#     print("\nreaction:", data['reaction'])
#     print("\nreaction:", sorted(data['reaction'], key=lambda k: k['name']))


class Graph:
    data = []
    Metabolites = []
    Reaction = []
    nodes_metabolites = []
    nodes_reactions = []
    edges = []
    meta_keyword = [] #liste of keyword during search
    reac_keyword = [] #liste temp pour garder les catégories pour reactions et metabolites
    G = nx.MultiDiGraph()

    #open the reference file and sort the metabolic and reaction by alphabetic order of ID.
    def LoadJson_and_sort(self, file):
        with open(file, "r") as json_file:
            self.data = json.load(json_file)



    def __init__(self, file):
        self.LoadJson_and_sort(file)

    def clear_data(self):
        self.Metabolites.clear()
        self.Reaction.clear()

    def print_data(self):
        print("\nmetabolites not sorted", self.data["metabolites"])
        print("\nreaction not sorted", self.data['reactions'])

    # def SortJson(self, file):
    #     self.Metabolites = sorted(file["metabolites"], key=lambda k: k["name"])
    #     print("\nmetabolites sorted", self.Metabolites)
    #     self.Reaction = sorted(file["reactions"], key=lambda k: k["name"])
    #     print("\nreaction sorted", self.Reaction)

    def meta_keyword_update(self,keyword):
        self.meta_keyword.append(keyword)

    def reac_keyword_update(self,keyword):
        self.reac_keyword.append(keyword)


    def create_nodes_metabolites(self):
        for item in self.Metabolites:
            item["size"] = 20
            item["group"] = 2
            item["title"] = item["id"]
            if "name" in item:
                del item["name"]
            self.nodes_metabolites.append((item['id'], item))
        print("\nmetabolites sorted for networkX ", self.nodes_metabolites)

    def create_nodes_reactions(self):
        for item in self.Reaction:
            item["size"] = 50
            item["group"] = 1
            item["title"] = item["id"]
            if "name" in item:
                del item["name"]
            self.nodes_reactions.append((item['id'], item))
        print("\nreaction sorted for networkX", self.nodes_reactions)


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


    # ------------------ ADD TEMPORARY FUNCTIONS TO SHOW GRAPHS ----------------------------- #

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
        # nt.show_buttons()
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
            "enabled": false,
            "minVelocity": 0.75
          }
        }
        """)
        nt.show('nx.html')

    def create_edges(self):
        for reaction in self.Reaction:
            for metabolite, stoech in reaction["metabolites"].items():
                if stoech > 0:
                    self.edges.append([reaction["id"], metabolite])
                if stoech < 0:
                    self.edges.append([metabolite, reaction["id"]])




    #base idea for dichotomic search
    #see if kept as it is
    """
    def Search(self, file, category, keyword):
        a = 0
        b = len(file)
        if b == 0:
            #cas où la liste est vide
            return False
        while b > a + 1:
            m = (a + b) // 2
            if t[m] > keyword:
                b = m
            else:
                a = m
        return t[a] == keyword
        """


if __name__ == '__main__':

    # with open('Test_glycolysis.json') as json_file:
    #     data = json.load(json_file)
    g = Graph('actinidia_chinensis_merged.json')
    # g.reac_keyword_update("RXN-20436")
    # g.reac_keyword_update("RXN-17864")
    g.search_reactions()
    # g.meta_keyword_update("CPD-253_c")
    # g.meta_keyword_update("L-DIHYDROXY-PHENYLALANINE_c")
    g.meta_keyword_update("ACP_c")
    g.search_metabolites()
    g.create_nodes_metabolites()
    g.create_nodes_reactions()
    g.create_edges()
    g.create_Graph()
    g.show_graph()