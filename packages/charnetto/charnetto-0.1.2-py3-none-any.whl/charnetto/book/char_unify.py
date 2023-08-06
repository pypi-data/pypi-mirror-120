import networkx as nx
import numpy as np
import pandas


def get_unif_df(df):
    """Unify tags for all occurrences of an entity"""
    mapping = df.groupby(["name"])["tag"].apply(lambda s: s.value_counts().idxmax())
    unif_df = df.copy()
    unif_df["utag"] = unif_df["name"].map(mapping)
    return unif_df


def get_char_list(unif_df):
    """Collect entities labelled as characters"""
    filt_df = unif_df[unif_df["utag"] == "PER"]
    char_list = filt_df["name"].value_counts()
    return char_list


def characters_pipeline(df):
    """Unify tags and collect entities labelled as characters"""
    unif_df = get_unif_df(df)
    char_list = get_char_list(unif_df)
    return char_list


def filter_char_list(char_list, min_occ):
    """Choose a minimum threshold of occurrences for the characters list"""
    top_char_list = char_list[char_list >= min_occ]
    return top_char_list


def find_links(char_list):
    """Link characters if an entity is totally embedded in another entity"""
    links = []
    position = []

    for i in range(len(char_list)):
        for j in range(len(char_list)):
            if i != j:
                name_i = char_list[i]
                name_j = char_list[j]
                if name_i in name_j:
                    link = name_i, name_j
                    links.append(link)

                    position.append(i)
                    position.append(j)

    position = np.unique(position)
    return links, position


def create_graph(char_list):
    """Generate a holoviews directed graph"""
    G = nx.DiGraph()
    G.add_nodes_from(char_list.index)
    links, _ = find_links(char_list.index)
    G.add_edges_from(links)
    return G


def get_char_graph(char_list, min_occ):
    """Create a graph based on a characters list"""
    top_char_list = filter_char_list(char_list, min_occ)
    G = create_graph(top_char_list)
    return G


def char_unif_pipeline(df, min_occ):
    """Unify the entities and map those related to the same character"""
    char_list = characters_pipeline(df)
    G = get_char_graph(char_list, min_occ)
    return G


def concat_parents(G):
    """Create lists of aliases for entities that are totally embedded in other entities"""
    graph_filtered_char_list = []

    for node in G.nodes():
        if list(G.successors(node)):
            continue

        current = [node, *G.predecessors(node)]
        graph_filtered_char_list.append(current)

    return graph_filtered_char_list


def write_charlist(output_path, concat_char_list):
    """Save concatenated list in structured text file"""
    with open(output_path, "w", encoding="utf-8") as file:
        for element in concat_char_list:
            if len(element) == 1:
                file.write(f"{element[0]}\n")
            elif len(element) > 1:
                file.write(f"{element[0]}\n")
                for el in element[1:]:
                    file.write(f"  {el}\n")


def concatenate_parents(df, min_occ):
    """Unify the entities and map those related to the same character.

    Tags unification: the function groups by name, then counts all different tags associated to the
    same entity and unifies them by taking the most used tag and replacing all tags
    by this one in a new column "utag".

    Graph creation: the function creates links between entities if one is embedded in another, then
    builds a graph to show the links between the entities. A list of aliases is then generated based
    on the hierarchy in the directed graph.

    Parameters
    ----------
    df: pandas.DataFrame
        The dataframe of all named entities occurrences.
    min_occ: int
        Threshold for the minimal amount of occurrences for each entity.
    """
    G = char_unif_pipeline(df, min_occ)
    concat_char_list = concat_parents(G)

    return concat_char_list
