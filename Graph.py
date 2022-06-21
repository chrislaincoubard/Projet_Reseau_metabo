import json
import networkx as nx
from pyvis.network import Network
from utils import *


class Graph:
    data = []  # data from Json used to initialize the graph
    Metabolites = []  # Metabolites added from search
    Reaction = []  # Reaction added from search
    compartment = []
    search_compartment = []
    nodes_metabolites = []
    nodes_reactions = []
    edges = []
    meta_keyword = []  # liste of keyword during search
    reac_keyword = []  # liste temp pour garder les catégories pour reactions et metabolites
    cofactors = ["CDP-CHOLINE_c", "CMP_c","PROTON_c","PPI_c","PROTOHEME_c","WATER_c",
                 "OXYGEN-MOLECULE_c","CARBON-DIOXIDE_c","NADPH_c","NADP_c","CMP_CCO-RGH-ER-LUM",
                 "PROTON_CCO-RGH-ER-LUM","Pi_c","AMP_c","Acceptor_c","CO-A_c","ATP_c","ADP_c","GDP_c",
                 "GTP_c","MG+2_c","PROTON_e","OXYGEN-MOLECULE_m","WATER_m","CARBON-MONOXIDE_c", "NAD_c", "NADH_c"]
    G = nx.MultiDiGraph()

    # open the reference file and stores the data as attribute.
    def Load_json(self, file):
        if file != "":
            with open(file, "r") as json_file:
                self.data = json.load(json_file)
            for comp in self.data["compartments"]:
                comp = cobra_compatibility(comp)
                self.compartment.append(comp)

    def cobra_compatibility(reaction, side=True):
        """Function to transform a reaction ID into a cobra readable ID and vice versa.

        PARAMS:
            reaction (str) -- the reaction.
            side (boolean) -- True if you want to convert a COBRA ID into a readable ID,
            False for the reverse.
        RETURNS:
            reaction (str) -- the transformed reaction.
        """

        if side:
            reaction = reaction.replace("__46__", ".").replace("__47__", "/").replace("__45__", "-") \
                .replace("__43__", "+").replace("__91__", "[").replace("__93__", "]")
            if re.search('(^_\d)', reaction):
                reaction = reaction[1:]
        else:
            reaction = reaction.replace("/", "__47__").replace(".", "__46__").replace("-", "__45__") \
                .replace("+", "__43__").replace("[", "__91__").replace("]", "__93")
            if re.search('(\d)', reaction[0]):
                reaction = "_" + reaction
        return reaction

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
        keyword = cobra_compatibility(keyword)
        if keyword not in self.meta_keyword:
            self.meta_keyword.append(keyword)
            return True
        if keyword in self.meta_keyword:
            self.meta_keyword.remove(keyword)
            return False

    def reac_keyword_update(self, keyword):
        keyword = cobra_compatibility(keyword)
        if keyword not in self.reac_keyword:
            self.reac_keyword.append(keyword)
            return True
        if keyword in self.reac_keyword:
            self.reac_keyword.remove(keyword)
            return False

    def compartment_update(self, keyword):
        keyword = cobra_compatibility(keyword)
        if keyword not in self.search_compartment :
            self.search_compartment.append(keyword)
            return True
        if keyword in self.search_compartment :
            self.search_compartment.remove(keyword)
            return False

    # create the list of nodes for the graph.
    # All info from Json file are added as nodes attributes + graphical attributes for visualization
    # Name key deleted from dictionnary because it causes conflict with netwrokx graph creation

    def create_nodes_metabolites(self, data):
        for item in data:
            if item["id"] not in self.cofactors:
                item["size"] = 20  # Size of the node
                item["group"] = 2  # Group of the node (to differentiate metabolites from reactions and cofactors)
                item["title"] = item["id"]  # Message displayed when node is hoverede by mouse
                item["color"] = "blue"
            else :
                item["size"] = 10  # Size of the node
                item["group"] = 3  # Group of the node (to differentiate metabolites from reactions and cofactors)
                item["title"] = item["id"]  # Message displayed when node is hoverede by mouse
            if "name" in item:
                del item["name"]
            self.nodes_metabolites.append((item['id'], item))

    # Similar to create_nodes_reactions
    def create_nodes_reactions(self, data):
        for item in data:
            item["size"] = 35
            item["group"] = 1
            item["shape"] = "diamond"
            item["title"] = item["gene_reaction_rule"].replace(" or ", " <br> ")
            if "name" in item:
                del item["name"]
            self.nodes_reactions.append((item['id'], item))

    # edges creating by creating a 2-tuple for each edge.
    # Tuple means = (starting_node, ending node)
    def create_edges(self, type, cofactor):
        for reaction in type:
            for metabolite, stoech in reaction["metabolites"].items():
                if not cofactor:
                    if metabolite not in self.cofactors:
                        if stoech > 0:
                            self.edges.append([reaction["id"], metabolite])
                        if stoech < 0:
                            self.edges.append([metabolite, reaction["id"]])
                else :
                    if stoech > 0:
                        self.edges.append([reaction["id"], metabolite])
                    if stoech < 0:
                        self.edges.append([metabolite, reaction["id"]])


    # search for metabolites based on list of metabo ID
    # add all the reactions connected to the searched metabolites and all the metabolites associated with the reactions.
    def search_metabolites(self, cofactor = True):
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
                        if not cofactor :
                            if item["id"] not in self.cofactors:
                                self.Metabolites.append(item)
                        else :
                            self.Metabolites.append(item)
        self.meta_keyword.clear()




    # search for reactions based on list of reaction ID
    # Add all the reactions and the meatbolites involved in them
    def search_reactions(self, cofactor):
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
                    if not cofactor:
                        if item["id"] not in self.cofactors:
                            self.Metabolites.append(item)
                    else:
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
        with open(name, 'w') as f:
            f.write(json.dumps(tot_dico))

    # ------------------ Functions to show graph ----------------------------- #

    def create_Graph(self,name,cofactor,physics ):
        # create or show graph wether a search has been made or not
        if self.meta_keyword or self.reac_keyword:  # if searched has been made.
            self.search_metabolites(cofactor)
            self.search_reactions(cofactor)
            self.create_nodes_metabolites(self.Metabolites)
            self.create_nodes_reactions(self.Reaction)
            self.create_edges(self.Reaction, cofactor)
            self.G.add_nodes_from(self.nodes_metabolites)
            self.G.add_nodes_from(self.nodes_reactions)
            self.G.add_edges_from(self.edges)
            self.show_graph(name,physics)
        else:  # create graph from all JSON if no search was made
            self.create_nodes_metabolites(self.data["metabolites"])
            self.create_nodes_reactions(self.data["reactions"])
            self.create_edges(self.data["reactions"],cofactor)
            self.G.add_nodes_from(self.nodes_metabolites)
            self.G.add_nodes_from(self.nodes_reactions)
            self.G.add_edges_from(self.edges)
            self.show_graph(name, physics)

    def show_graph(self, name, option):
        nt = Network("1000px", "1000px")
        nt.from_nx(self.G,show_edge_weights=False)
        nt.toggle_hide_edges_on_drag(True)
        nt.set_edge_smooth("vertical")
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
                "minVelocity": 0.75,
                "enabled" : false
              }
            }
            """)
        nt.show(name)
