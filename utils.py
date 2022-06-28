import re
import json
import os
import csv


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


def get_metacyc_ids(data, path):
    """Function to make the correspondence file between short and long ID of Metacyc."""

    res = []
    print("Number of reactions found in the metacyc.json file : {}", format(len(data["reactions"])))
    for reaction in data["reactions"]:
        long_id = reaction["name"].split("/")[0]
        # Getting rid of the brackets in the name sometimes!
        reaction_pattern = re.compile('([[].*[]])')
        tmp_id = reaction_pattern.sub("", long_id)
        short_id = tmp_id
        # Regexp to "clean" the metabolite's names
        meta_pattern = re.compile('(_CC[OI]-.*)|(^[_])|([_]\D$)')
        if len(reaction["metabolites"].keys()) != 0:
            for metabolite in reaction["metabolites"].keys():
                # The metabolite is "cleaned" here
                metabolite = meta_pattern.sub("", metabolite)
                len_id, len_meta = len(tmp_id), len(metabolite)
                diff = len_id - len_meta
                # Small trick to get only the end of the ID removed and not the beginning
                # (metabolite's names can be in the reaction's name)
                test_id = tmp_id[:diff - 1] + tmp_id[diff - 1:].replace("-" + metabolite, "")
                if len(test_id) < len(short_id):
                    short_id = test_id
            res.append([short_id, reaction["name"]])
    write_csv(path, "/metacyc_ids", res, "\t")


def get_metacyc_ids_metabolites(metabolite):
    meta_pattern = re.compile('(_CC[OI]-.*)|(^[_])|([_]\D$)')
    return meta_pattern.sub("", metabolite)


def load_json(file):
    with open(file, "r") as json_file:
        data = json.load(json_file)
    return data


def write_csv(directory, name, list_value, separator=","):
    """Function to save a file as a CSV format, needs a list of lists,
    first list as the column names."""

    if separator == "\t":
        extension = ".tsv"
    else:
        extension = ".csv"
    with open(slash(directory) + name + extension, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=separator)
        for f in list_value:
            writer.writerow(f)


def slash(directory):
    """Utility function to put a slash after a directory path if needed."""

    if directory[-1] != "/":
        return directory + "/"
    else:
        return directory


def read_file_listed(path):
    """Function to read and return a file line by line in a list."""

    f = open(path, "r")
    res = f.readlines()
    f.close()
    return res


def build_correspondence_dict(path, sep="\t"):
    """Function to create a dictionary of correspondence between
    elements from a correspondence file (Metacyc short and long IDs for example).
    PARAMS:
        path (str) -- the path to the csv/tsv file containing the corresponding information (only two elements).
        sep (str) -- the separator of the correspondence file (default = tab).
    RETURNS:
        matching_dict -- dictionary with an element as key that matches the value.
        matching_dict_reversed -- same thing as matching_dict but in reversed (value is key and vice-versa).
    """

    matching = read_file_listed(path)
    matching_dict = {}
    matching_dict_reversed = {}
    for line in matching:
        if line:
            couple = line.rstrip().split(sep)
            if couple[0] in matching_dict.keys():
                matching_dict[couple[0]].append(couple[1])
            else:
                matching_dict[couple[0]] = [couple[1]]
            matching_dict_reversed[couple[1]] = couple[0]
    return matching_dict, matching_dict_reversed
