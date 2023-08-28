import os
from typing import List

import networkx as nx
from networkx import DiGraph, read_gexf
from networkx.algorithms.community import louvain_communities


def getCommunities(graph: DiGraph) -> List[set[int]]:
    """

    :param graph: DiGraph:
    :param graph: DiGraph:
    :param graph: DiGraph:
    :param graph: DiGraph:
    :param graph: DiGraph:
    :param graph: DiGraph:
    :param graph: DiGraph:

    """
    communitySubgraphs: List[nx.Graph] = []
    communities: List[set[int]] = louvain_communities(graph, seed=None)

    for community in communities:
        subgraph = graph.subgraph(community).copy()
        communitySubgraphs.append(subgraph)

    return communitySubgraphs


def createSubgraphs(graph: DiGraph, communities: List[set[int]]):
    """

    :param graph: DiGraph:
    :param communities: List[set[int]]:
    :param graph: DiGraph:
    :param communities: List[set[int]]:
    :param graph: DiGraph:
    :param communities: List[set[int]]:
    :param graph: DiGraph:
    :param communities: List[set[int]]:
    :param graph: DiGraph:
    :param communities: List[set[int]]:
    :param graph: DiGraph:
    :param communities: List[set[int]]:
    :param graph: DiGraph:
    :param communities: List[set[int]]:

    """
    folderPath = "/Users/karolinaryzka/Documents/dnn-dependencies/dnn_dependencies/subgraphs/felflare-bert-restore-punctuation"
    for i, community in enumerate(communities):
        filePath = os.path.join(folderPath, f"{i}.gexf")
        nx.write_gexf(community, filePath)


def main() -> None:
    """ """
    graph: DiGraph = read_gexf("felflare-bert-restore-punctuation.gexf")
    communities = getCommunities(graph)
    createSubgraphs(graph, communities)


main()
