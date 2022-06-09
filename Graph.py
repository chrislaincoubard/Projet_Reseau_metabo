import json
import networkx as nx
from pyvis.network import Network


class Graph:
    data = []  # data from Json used to initialize the graph
    Metabolites = []  # Metabolites added from search
    Reaction = []  # Reaction added from search
    compartment = []
    nodes_metabolites = []
    nodes_reactions = []
    edges = []
    meta_keyword = []  # liste of keyword during search
    reac_keyword = []  # liste temp pour garder les catégories pour reactions et metabolites
    G = nx.MultiDiGraph()

    # open the reference file and stores the data as attribute.
    def Load_json(self, file):
        if file != "":
            with open(file, "r") as json_file:
                self.data = json.load(json_file)

    def __init__(self, file=None):
        if file is not None:
            self.Load_json(file)
        else:
            self.data = []

    # clear data from current instance, used for GUI implementation where only one graphe instance is used.
    def clear_data(self):
        self.Metabolites.clear()
        self.Reaction.clear()
        self.edges.clear()
        self.G.clear()
        self.nodes_reactions.clear()
        self.nodes_metabolites.clear()
        self.meta_keyword.clear()
        self.reac_keyword.clear()
        self.compartment.clear()

    def meta_keyword_update(self, keyword):
        if keyword not in self.meta_keyword:
            self.meta_keyword.append(keyword)

    def reac_keyword_update(self, keyword):
        if keyword not in self.reac_keyword:
            self.reac_keyword.append(keyword)

    def compartment_update(self, keyword):
        if keyword not in self.compartment :
            self.compartment.append(keyword)

    # create the list of nodes for the graph.
    # All info from Json file are added as nodes attributes + graphical attributes for visualization
    # Name key deleted from dictionnary because it causes conflict with netwrokx graph creation

    def create_nodes_metabolites(self, data):
        for item in data:
            item["size"] = 20  # Size of the node
            item["group"] = 2  # Group of the node (to differentiate metabolites from reactions
            item["title"] = item["id"]  # Message displayed when node is hoverede by mouse
            if "name" in item:
                del item["name"]
            self.nodes_metabolites.append((item['id'], item))

    # Similar to create_nodes_reactions
    def create_nodes_reactions(self, data):
        for item in data:
            item["size"] = 50
            item["group"] = 1
            item["title"] = item["gene_reaction_rule"].replace(" or ", " <br> ")
            if "name" in item:
                del item["name"]
            self.nodes_reactions.append((item['id'], item))

    # edges creating by creating a 2-tuple for each edge.
    # Tuple means = (starting_node, ending node)
    def create_edges(self, type):
        for reaction in type:
            for metabolite, stoech in reaction["metabolites"].items():
                if stoech > 0:
                    self.edges.append([reaction["id"], metabolite])
                if stoech < 0:
                    self.edges.append([metabolite, reaction["id"]])

    # search for metabolites based on list of metabo ID
    # add all the reactions connected to the searched metabolites and all the metabolites associated with the reactions.
    def search_metabolites(self):
        if not self.meta_keyword:
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

    # search for reactions based on list of reaction ID
    # Add all the reactions and the meatbolites involved in them
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

    # ------------------ Function to save graphs ------------------- #

    # Remove the graphical attribute from nodes
    # Keep the structure from the initial JSON file
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
        if "." in name:
            extension = name.split('.')
            if "json" == extension[1]:
                with open(name, 'w') as f:
                    f.write(json.dumps(tot_dico))
            else:
                extension[1] = ".json"
                with open(extension[0] + extension[1], 'w') as f:
                    f.write(json.dumps(tot_dico))
        else:
            with open(name + ".json", 'w') as f:
                f.write(json.dumps(tot_dico))


    # ------------------ Functions to show graph ----------------------------- #

    def create_Graph(self, name,option=1):
        # create or show graph depending if a search has been made
        if self.meta_keyword or self.reac_keyword:  # if searched has been made.
            self.search_metabolites()
            self.search_reactions()
            self.create_nodes_metabolites(self.Metabolites)
            self.create_nodes_reactions(self.Reaction)
            self.create_edges(self.Reaction)
            self.G.add_nodes_from(self.nodes_metabolites)
            self.G.add_nodes_from(self.nodes_reactions)
            self.G.add_edges_from(self.edges)
            if "." in name:
                extension = name.split('.')
                if "html" == extension[1]:
                    self.show_graph(name, option)
                else:
                    extension[1] = ".html"
                    self.show_graph(extension[0] + extension[1], option)
            else:
                self.show_graph(name + ".html",option)
        else:  # create graphe from all JSON if no search was made
            self.create_nodes_metabolites(self.data["metabolites"])
            self.create_nodes_reactions(self.data["reactions"])
            self.create_edges(self.data["reactions"])
            self.G.add_nodes_from(self.nodes_metabolites)
            self.G.add_nodes_from(self.nodes_reactions)
            self.G.add_edges_from(self.edges)
            if "." in name:
                extension = name.split('.')
                if "html" == extension[1]:
                    self.show_graph(name, option)
                else:
                    extension[1] = ".html"
                    self.show_graph(extension[0] + extension[1], option)
            else:
                self.show_graph(name + ".html",option)

    def show_graph(self, name, option):
        nt = Network("1000px", "1000px")
        nt.from_nx(self.G)
        nt.toggle_hide_edges_on_drag(True)
        nt.set_edge_smooth("dynamic")
        # Set_graphical options to allow good representation of graph
        if option == 1:
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
        if option == 2:
            nt.show_buttons(filter_=["physics"])
        if option == 3:
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
                            "enabled": False
                          }
                        }
                        """)
        nt.show(name)
