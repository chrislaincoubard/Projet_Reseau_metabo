import json
import networkx as nx
import time
from pyvis.network import Network

def load_json(file):
    with open(file, "r") as f:
        data = json.load(f)
    return data

def load_graph(file):
    data = load_json(file)
    edges = create_edges(data)
    nodes_m = create_nodes(data,"metabolites")
    nodes_r = create_nodes(data,"reactions")
    G = create_Graph(nodes_r, nodes_m,edges)
    show_graph(G)



def create_edges(data):
    edges = []
    for reaction in data["reactions"]:
        for metabolite, stoech in reaction["metabolites"].items():
            if stoech > 0:
                edges.append([reaction["id"],metabolite])
            if stoech < 0:
                edges.append([metabolite,reaction["id"]])
    return tuple(edges)


# def create_nodes_metabolites(data,type):





def create_nodes(data,type):
    """
        Create a list of nodes for the graph, distinguish between metabolites and reactions. Format to be ready to use in netwrokX graph.
        :param data: from json file
        :param type: String : most likely either "metabolites" or "reactions"
        :return: list in of tuples with (nodes, nodes_dict_attributes) to be integrated in Networkx
    """
    nodes = []
    for item in data[type]:
        if type == "metabolites":
            item["size"] = 20
            item["group"] = 2
            item["title"] = item["id"]
            del item["name"]
            nodes.append((item['id'],item))
        if type == "reactions":
            item["size"] = 50
            item["group"] = 1
            item["title"] = item["id"]
            del item["name"]
            nodes.append((item['id'], item))
    return nodes


def save_graph_json(name,metabolites,reactions): #not working properly still
    print(metabolites)
    tot_dico = {}
    meta = []
    reac = []
    for item in metabolites:
        meta.append(item[1])
    for item in reactions :
        meta.append(item[1])
    tot_dico["reactions"]=reactions
    with open(name, 'w') as f:
        f.write(json.dumps(tot_dico))






def create_Graph(nodes_r,nodes_m,edges):
    G=nx.MultiDiGraph()
    G.add_nodes_from(nodes_m)
    G.add_nodes_from(nodes_r)
    G.add_edges_from(edges)
    return G

def show_graph(Graph):
    nt = Network("750px", "750px")
    nt.from_nx(Graph)
    nt.show_buttons()
    nt.toggle_hide_edges_on_drag(True)
    nt.set_edge_smooth("straightCross")
    nt.show('nx.html')





if __name__ == '__main__':
    start_time = time.process_time()
    data = load_json("Test_glycolysis.json")
    # load_graph("Testing_write.json")
    meta = create_nodes(data,"metabolites")
    # print(meta)
    reac = create_nodes(data,"reactions")
    save_graph_json("Testing_write.json",meta,reac)
    # load_graph("Testing_write.json")

    print("---- %s s -----" % (time.process_time()-start_time))
