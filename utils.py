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