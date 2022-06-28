import webbrowser

import networkx as nx
from pyvis.network import Network
from utils import *
import random as rd

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
    cofactors = ["CDP-CHOLINE_c", "CMP_c", "PROTON_c", "PPI_c", "PROTOHEME_c", "WATER_c",
                 "OXYGEN-MOLECULE_c", "CARBON-DIOXIDE_c", "NADPH_c", "NADP_c", "CMP_CCO-RGH-ER-LUM",
                 "PROTON_CCO-RGH-ER-LUM", "Pi_c", "AMP_c", "Acceptor_c", "CO-A_c", "ATP_c", "ADP_c", "GDP_c",
                 "GTP_c", "MG+2_c", "PROTON_e", "OXYGEN-MOLECULE_m", "WATER_m", "CARBON-MONOXIDE_c", "NAD_c", "NADH_c"]
    G = nx.MultiDiGraph()
    corresp_dict_reac = {}
    reversed_corresp_dict_reac = {}

    def update_data(self, file):
        self.data = load_json(file)
        get_metacyc_ids(self.data, os.path.dirname(file))
        self.corresp_dict_reac, self.reversed_corresp_dict_reac = build_correspondence_dict(os.path.dirname(file) + "\\metacyc_ids.tsv")
        for comp in self.data["compartments"]:
            comp = cobra_compatibility(comp)
            self.compartment.append(comp)


    def __init__(self, file=""):
        if file != "":
            self.data = load_json(file)
            for comp in self.data["compartments"]:
                comp = cobra_compatibility(comp)
                self.compartment.append(comp)
            get_metacyc_ids(self.data, os.path.dirname(file))
        else:
            self.data = []

    # clear data from current instance, used for GUI implementation where only one graphe instance is used.
    def clear_data(self):
        self.Metabolites.clear()
        self.Reaction.clear()
        self.edges.clear()
        self.nodes_reactions.clear()
        self.nodes_metabolites.clear()
        self.meta_keyword.clear()
        self.reac_keyword.clear()
        self.search_compartment.clear()

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
        if keyword not in self.search_compartment:
            self.search_compartment.append(keyword)
            return True
        if keyword in self.search_compartment:
            self.search_compartment.remove(keyword)
            return False

    # create the list of nodes for the graph.
    # All info from Json file are added as nodes attributes + graphical attributes for visualization
    # Name key deleted from dictionnary because it causes conflict with netwrokx graph creation

    def create_nodes_metabolites(self, data):
        for item in data:
            if item["id"] not in self.cofactors:
                item["size"] = 20  # Size of the node
                item["group"] = "metabolites"  # Group of the node (to differentiate metabolites from reactions and cofactors)
                item["title"] = item["id"]  # Message displayed when node is hoverede by mouse
                item["mass"] = 2
            else:
                item["size"] = 10  # Size of the node
                item["group"] = "cofactors"  # Group of the node (to differentiate metabolites from reactions and cofactors)
                item["title"] = item["id"]  # Message displayed when node is hoverede by mouse
                item["mass"] = 0.5
                item["physics"] = False
            if "name" in item:
                del item["name"]
            self.nodes_metabolites.append((item['id'], item))

    # Similar to create_nodes_reactions
    def create_nodes_reactions(self, data):
        for item in data:
            # test to add node size scaling depending on a specified value.
            # It works but override the size attribute of the node.
            # rand = rd.uniform(0.5,1.0)
            # item["value"] = rand
            item["size"] = 35
            item["group"] = "reactions"
            item["shape"] = "diamond"
            item["mass"] = 5
            item["title"] = item["gene_reaction_rule"].replace(" or ", " <br> ")
            if "name" in item:
                del item["name"]
            self.nodes_reactions.append((item['id'], item))

    def create_legends_nodes(self, cofactor):
        """
        Trick to add legend to the graph because it seems you cannot add it from the template for some reasons
        :param cofactor: boolean ; If true, add the cofactor legend
        """
        if cofactor :
            nodes = ["reactions", "metabolites", "cofactors"]
            pos = [[-600,-500], [-600,-400], [-600, -300]]
        else :
            nodes = ["reactions", "metabolites"]
            pos = [[-600,-500 ], [-600, -400]]
        legend_nodes = [
            (
                legend_node,
                {
                    'group': str(legend_node),
                    'label': str(legend_node),
                    'size': 30,
                    'fixed': True,
                    'physics': False,
                    'x': pos[0],
                    'y': pos[1],
                    'shape': 'box',
                    'widthConstraint': 100,
                    'font': {'size': 20}
                }
            )
            for legend_node, pos in zip(nodes,pos)
        ]
        return legend_nodes


    def create_edges(self, type, cofactor):
        for reaction in type:
            for metabolite, stoech in reaction["metabolites"].items():
                if not cofactor:
                    if metabolite not in self.cofactors:
                        if stoech > 0:
                            self.edges.append((reaction["id"], metabolite))
                        if stoech < 0:
                            self.edges.append((metabolite, reaction["id"]))
                else:
                    if stoech > 0:
                        self.edges.append((reaction["id"], metabolite))
                    if stoech < 0:
                        self.edges.append((metabolite, reaction["id"]))

    # search for metabolites based on list of metabo ID
    # add all the reactions connected to the searched metabolites and all the metabolites associated with the reactions.
    def search_metabolites(self, cofactor):
        if not self.meta_keyword:
            return None
        temp_meta = {}
        temp_keyword =[]
        for key in self.meta_keyword:
            for reac in self.data["reactions"]:
                if key in reac["metabolites"] and reac not in self.Reaction:
                    reac["id"] = self.reversed_corresp_dict_reac[reac["id"].strip("_")]
                    self.Reaction.append(reac)
                    temp_meta = reac["metabolites"]
                for meta in self.data["metabolites"]:
                    if meta["id"] in temp_meta.keys() and meta not in self.Metabolites:
                        if not cofactor:
                            if meta["id"] not in self.cofactors:
                                self.Metabolites.append(meta)
                        else:
                            self.Metabolites.append(meta)


    # search for reactions based on list of reaction ID
    # Add all the reactions and the meatbolites involved in them
    def search_reactions(self, cofactor):
        if not self.reac_keyword:
            return None
        temp_meta = {}
        for key in self.reac_keyword:
            for reac in self.data["reactions"]:
                if reac["id"] == key and reac not in self.Reaction:
                    reac["id"] = self.reversed_corresp_dict_reac[reac["id"].strip("_")]
                    self.Reaction.append(reac)
                    temp_meta = reac["metabolites"]
            for meta in self.data["metabolites"]:
                if meta["id"] in temp_meta.keys() and meta not in self.Metabolites:
                    if not cofactor:
                        if meta["id"] not in self.cofactors:
                            self.Metabolites.append(meta)
                    else:
                        self.Metabolites.append(meta)

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

    def create_Graph(self, name, cofactor, physics):
        # create or show graph wether a search has been made or not
        if self.meta_keyword or self.reac_keyword:  # if searched has been made.
            self.search_metabolites(cofactor)
            self.search_reactions(cofactor)
            self.create_nodes_metabolites(self.Metabolites)
            self.create_nodes_reactions(self.Reaction)
            self.create_edges(self.Reaction, cofactor)
            self.G.add_nodes_from(self.nodes_metabolites)
            self.G.add_nodes_from(self.nodes_reactions)
            self.G.add_nodes_from(self.create_legends_nodes(cofactor))
            for start, finish in self.edges:
                if start in self.cofactors or finish in self.cofactors:
                    self.G.add_edge(start, finish, physics=False, dashes=True)
                else:
                    self.G.add_edge(start, finish, physics=True, width=3)
            self.show_graph(name, physics)
        else:  # create graph from all JSON if no search was made
            self.create_nodes_metabolites(self.data["metabolites"])
            self.create_nodes_reactions(self.data["reactions"])
            self.create_edges(self.data["reactions"], cofactor)
            self.G.add_nodes_from(self.nodes_metabolites)
            self.G.add_nodes_from(self.nodes_reactions)
            self.G.add_edges_from(self.edges, physics=False)
            self.G.add_nodes_from(self.create_legends_nodes(True))
            self.show_graph(name, physics)

    def show_graph(self, name, option):
        nt = Network("1000px", "1000px")
        nt.set_template("PlantGEM_template.html")
        nt.from_nx(self.G, show_edge_weights=False)
        nt.toggle_hide_edges_on_drag(True)
        nt.set_edge_smooth("vertical")
        # Set_graphical options to try to have good representation of graph
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
                "selectionWidth": 5,
                "smooth": {
                  "type": "vertical",
                  "forceDirection": "none"
                }
              },
              "physics": {
                "barnesHut": {
                  "gravitationalConstant": -1500
                },
                "minVelocity": 0.75
              }
            }""")
        if option == 2:
            nt.show_buttons(filter_=["physics", "nodes", "edges"])
        if option == 3:
            nt.set_options("""
            var options = {
            "nodes": {
                "borderWidthSelected": 5
               },
              "edges": {
              "selectionWidth": 5,
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
        nt.write_html(name)
        webbrowser.open(name)
