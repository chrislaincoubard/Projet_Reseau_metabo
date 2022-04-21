import json


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
    keyword = [] #liste of keyword during search
    #liste temp pour garder les catégories pour reactions et metabolites

    #open the reference file and sort the metabolic and reaction by alphabetic order of ID.
    def LoadJson_and_sort(self, file):
        with open(file, "r") as json_file:
            data = json.load(json_file)
            self.Metabolites = sorted(data["metabolites"], key=lambda k: k["id"])
            self.Reaction = sorted(file["reactions"], key=lambda k: k["id"])

    def __init__(self, file):
        self.LoadJson_and_sort(file)

    def print_data(self):
        print("\nmetabolites not sorted", self.data['metabolites'])
        print("\nreaction not sorted", self.data['reactions'])

    # def SortJson(self, file):
    #     self.Metabolites = sorted(file["metabolites"], key=lambda k: k["name"])
    #     print("\nmetabolites sorted", self.Metabolites)
    #     self.Reaction = sorted(file["reactions"], key=lambda k: k["name"])
    #     print("\nreaction sorted", self.Reaction)

    def keyword_update(self,keyword):
        self.keyword.append(keyword)

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

    #a voir
    #permet de réduire les listes de metabolites et reactions avec seulement les éléments qui matchent tous les keywords
    def search_metabolites(self,metabolite):
        for key in self.keyword:
            for item in self.Metabolites:
                if item["id"] != metabolite:
                    self.Metabolites.remove(item)
            for item in self.Reaction:
                if metabolite not in item["metabolites"]:
                    self.Reaction.remove(item)



    #base idea for dichotomic search
    #see if kept as it is
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


if __name__ == '__main__':

    with open('Test_glycolysis.json') as json_file:
        data = json.load(json_file)
    g = Graph('Test_glycolysis.json')
    g.print_data()
    g.SortJson(data)
    g.create_nodes_metabolites()
    g.create_nodes_reactions()