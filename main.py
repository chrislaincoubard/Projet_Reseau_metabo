import json
import pprint
from operator import itemgetter

#from glyco import metabolites
with open('Test_glycolysis.json') as json_file:
    data = json.load(json_file)

    print("Type:", type(data))

    print("\nmetabolites:", data['metabolites'])
    print("\nreaction:", data['reaction'])
    print(type(data['metabolites']))

def recherche_dichotomique(element, liste_triee):
    a = 0
    b = len(liste_triee)-1
    m = (a+b)//2
    while a < b :
        if liste_triee[m] == element:
            return m
        elif liste_triee[m] > element:
            b = m-1
        else :
            a = m+1
        m = (a+b)//2
    return a

# codes = {
#     "Y": "Titre Y",
#     "B": "Titre B",
#     "A": "Titre A",
#     "D": "Titre D"
# }
#
# parts = [
#     {"id": "A-004", "name": "Foo"},
#     {"id": "D-142", "name": "Foo"},
#     {"id": "B-044", "name": "Foo"},
#     {"id": "Y-002", "name": "Foo"},
#     {"id": "D-024", "name": "Foo"},
# ]
# what_I_get = {}
# for code in codes:
#     what_I_get[code] = []
#     for part in parts:
#         if part["id"][0] == code:
#             what_I_get[code].append(part)
#     what_I_get[code] = sorted(what_I_get[code], key=lambda part: part["id"])
#
# print (what_I_get)

# d1 = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'a1': 5, 'b1': 10, 'c1': 8, 'd1': 6}
# print(d1)
# print(sorted(d1))
#tri(d1)

def tri(dico):
    #sorted(dico, key=lambda d: d['name'])
    sorted(dico, key=itemgetter('name'), reverse=True)
    #sorted(d1.items(), key=lambda t: t[0])
    return dico

#pprint.pprint(metabolites, width=5)

print("ok")
print(data['metabolites'])
print(tri(data['metabolites']))

print(sorted(data['metabolites'], key=lambda k: k['name']))
##################################################################################
my_list = [{'name':'Homer', 'age':39}, {'name':'Bart', 'age':10}]

#my_list.sort(lambda x,y : cmp(x['name'], y['name']))

print(sorted(my_list, key=lambda k: k['name']))