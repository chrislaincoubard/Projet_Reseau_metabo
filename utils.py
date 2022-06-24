import re

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

def get_metacyc_ids(reaction):
    """Function to conver long ID of Metacyc to short ID."""
    long_id = reaction['id'].split("/")[0]
    # Getting rid of the brackets in the name sometimes!
    reaction_pattern = re.compile('([[].*[]])')
    tmp_id = reaction_pattern.sub("", long_id)
    short_id = tmp_id
    # Regexp to "clean" the metabolite's names
    meta_pattern = re.compile('(_CC[OI]-.*)|(^[_])|([_]\D$)')
    if len(reaction["metabolites"].keys()) != 0:
        for metabolite in reaction["metabolites"].keys():
            # The metabolite are "cleaned" here
            metabolite = meta_pattern.sub("", metabolite)
            len_id, len_meta = len(tmp_id), len(metabolite)
            diff = len_id - len_meta
            # Small trick to get only the end of the ID removed and not the beginning
            # (metabolite's names can be in the reaction's name)
            test_id = tmp_id[:diff - 1] + tmp_id[diff - 1:].replace("-" + metabolite, "")
            if len(test_id) < len(short_id):
                short_id = test_id
        reaction["id"] = short_id
        return reaction


