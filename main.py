import json


with open('Test_glycolysis.json') as json_file:
    data = json.load(json_file)

#     print("Type:", type(data))
#     print(type(data['metabolites']))
#     print("\nmetabolites:", data['metabolites'])
#     print("\nmetabolites:", sorted(data['metabolites'], key=lambda k: k['name']))
#     print("\nreaction:", data['reaction'])
#     print("\nreaction:", sorted(data['reaction'], key=lambda k: k['name']))


class Graph:
    data = {}
    Metabolites = []
    Reaction = []
    nodes_metabolites = []
    nodes_reactions = []
    edges = []

    def LoadJson(self, file):
        with open(file, "r") as json_file:
            self.data = json.load(json_file)

    def __init__(self, file):
        self.LoadJson(file)

    def print_data(self):
        print("\nmetabolites not sorted", self.data['metabolites'])
        print("\nreaction not sorted", self.data['reaction'])

    def SortJson(self, file):
        self.Metabolites = sorted(file["metabolites"], key=lambda k: k["name"])
        print("\nmetabolites sorted", self.Metabolites)
        self.Reaction = sorted(file["reaction"], key=lambda k: k["name"])
        print("\nreaction sorted", self.Reaction)

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



g = Graph('Test_glycolysis.json')

g.print_data()
g.SortJson(data)
g.create_nodes_metabolites()
g.create_nodes_reactions()



