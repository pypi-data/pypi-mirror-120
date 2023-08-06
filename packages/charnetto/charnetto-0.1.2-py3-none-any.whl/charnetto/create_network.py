from collections import Counter
import networkx as nx
import json
import numpy as np


def create_graph(char_list, pairs):
    """Generate a weighted networkx graph"""
    G = nx.Graph()
    G.add_nodes_from(char_list)
    G.add_weighted_edges_from(pairs)
    return G


def create_charnet(pairs, min_pairs):
    """Create a character network based on a list of pairs.

    The pairs represent cooccurrences within the text, and
    a threshold can be fixed to ensure each cooccurrence
    appears at least min_pairs times.

    Parameters
    ----------
    pairs: list of lists
        The list of cooccurrences between two characters.
    min_pairs: int
        Threshold for minimum amount of occurrences of the same pair.
    """
    pairs = [sorted(pair) for pair in pairs]
    counter = Counter(map(tuple, pairs))

    triplets = []
    char_nodes = []
    for (a, b), value in counter.items():
        if value >= min_pairs:
            triplet = a, b, value
            triplets.append(triplet)
            char_nodes.append(a)
            char_nodes.append(b)
    char_nodes = np.unique(char_nodes)

    G = create_graph(char_nodes, triplets)

    return G
