import random
from typing import List, Literal, Set

import numpy
from networkx import *
from networkx.algorithms import *
from networkx.algorithms.approximation import *
from networkx.algorithms.assortativity import *
from networkx.algorithms.bipartite import robins_alexander_clustering
from networkx.algorithms.community import louvain_communities
from networkx.algorithms.components import *
from networkx.algorithms.threshold import is_threshold_graph
from networkx.exception import NetworkXNoPath, NetworkXNotImplemented

RANDOM_SEED: int = 42

random.seed(a=RANDOM_SEED, version=2)
numpy.random.seed(seed=RANDOM_SEED)


def computeBarycenter(graph: DiGraph) -> int:
    """


    :param graph: DiGraph:
    :param bar: Bar:

    """
    try:
        value: int = len(barycenter(G=graph))
    except NetworkXNoPath:
        value: int = -1
    return value


def computeRadius(graph: DiGraph) -> int:
    """


    :param graph: DiGraph:
    :param bar: Bar:

    """
    try:
        value: int = radius(G=graph)
    except NetworkXError:
        value: int = -1
    return value


def computeDAGLongestPathLength(graph: DiGraph) -> int:
    """


    :param graph: DiGraph:
    :param bar: Bar:

    """
    value: int = dag_longest_path_length(G=graph)
    return value


def computeAverageShortestPathLength(graph: DiGraph) -> float:
    """


    :param graph: DiGraph:
    :param bar: Bar:

    """
    value: float = average_shortest_path_length(G=graph)
    return value


def computeNumberOfIsolates(graph: DiGraph) -> int:
    """


    :param graph: DiGraph:
    :param bar: Bar:

    """
    value: int = number_of_isolates(G=graph)
    return value


def checkIsTriad(graph: DiGraph) -> int:
    """


    :param graph: DiGraph:
    :param bar: Bar:

    """
    value: int = int(is_triad(G=graph))
    return value


def checkIsThresholdGraph(graph: DiGraph) -> int:
    """


    :param graph: DiGraph:
    :param bar: Bar:

    """
    value: int = int(is_threshold_graph(G=graph))
    return value


def checkIsRegular(graph: DiGraph) -> int:
    """


    :param graph: DiGraph:
    :param bar: Bar:

    """
    value: int = int(is_regular(G=graph))
    return value


def checkIsPlanar(graph: DiGraph) -> int:
    """


    :param graph: DiGraph:
    :param bar: Bar:

    """
    value: int = int(is_planar(G=graph))
    return value


def checkIsDistanceRegular(graph: DiGraph) -> int:
    """


    :param graph: DiGraph:
    :param bar: Bar:

    """
    try:
        value: int = int(is_distance_regular(G=graph))
    except NetworkXNotImplemented:
        value: int = -1
    return value


def checkIsStronglyRegular(graph: DiGraph) -> int:
    """


    :param graph: DiGraph:
    :param bar: Bar:

    """
    try:
        value: int = int(is_strongly_regular(G=graph))
    except NetworkXNotImplemented:
        value: int = -1
    return value


def checkIsBipartite(graph: DiGraph) -> int:
    """


    :param graph: DiGraph:
    :param bar: Bar:

    """
    value: int = int(is_bipartite(G=graph))
    return value


def computeRobinsAlexanderClustering(graph: DiGraph) -> float | Literal[0]:
    """


    :param graph: DiGraph:
    :param bar: Bar:

    """
    value: float | Literal[0] = robins_alexander_clustering(G=graph)
    return value


def computeTransitivity(graph: DiGraph) -> float | Literal[0]:
    """


    :param graph: DiGraph:
    :param bar: Bar:

    """
    try:
        value: float | Literal[0] = transitivity(G=graph)
    except NetworkXNotImplemented:
        value: float = -1.0
    return value


def checkIsAperiodic(graph: DiGraph) -> int:
    """


    :param graph: DiGraph:
    :param bar: Bar:

    """
    value: int = int(is_aperiodic(G=graph))
    return value


def checkIsDirectedAcyclicGraph(graph: DiGraph) -> int:
    """


    :param graph: DiGraph:
    :param bar: Bar:

    """
    value: int = int(is_directed_acyclic_graph(G=graph))
    return value


def computeNumberOfNodes(graph: DiGraph) -> int:
    """


    :param graph: DiGraph:
    :param bar: Bar:

    """
    value: int = graph.number_of_nodes()
    return value


def computeDensity(graph: DiGraph) -> float:
    """


    :param graph: DiGraph:
    :param bar: Bar:

    """
    value: int = density(G=graph)
    return value


def computeNumberOfEdges(graph: DiGraph) -> int:
    """


    :param graph: DiGraph:
    :param bar: Bar:

    """
    value: int = graph.number_of_edges()
    return value


def computeNumberOfCommunities(graph: DiGraph) -> int:
    """


    :param graph: DiGraph:
    :param bar: Bar:

    """
    communities: List[Set[str]] = louvain_communities(graph, seed=42)
    value: int = len(communities)
    return value


def computeDiameter(graph: DiGraph) -> int:
    """


    :param graph: DiGraph:
    :param bar: Bar:

    """
    value: int = diameter(G=graph)
    return value


def computeDegreeAssortativityCoefficient(graph: DiGraph) -> float:
    """


    :param graph: DiGraph:
    :param bar: Bar:

    """
    value: float = degree_assortativity_coefficient(G=graph, x="out", y="in")
    return value


def computeAttributeAssortativityCoefficient(graph: DiGraph) -> float:
    """


    :param graph: DiGraph:
    :param bar: Bar:

    """
    value: float = attribute_assortativity_coefficient(
        G=graph,
        attribute="Operation_Type",
    )
    return value


def computeDegreePearsonCorrelationCoefficient(graph: DiGraph) -> float:
    """


    :param graph: DiGraph:
    :param bar: Bar:

    """
    value: float = degree_pearson_correlation_coefficient(
        G=graph,
        x="out",
        y="in",
    )
    return value


def checkIsSemiconnected(graph: DiGraph) -> int:
    """


    :param graph: DiGraph:
    :param bar: Bar:

    """
    value: int = int(is_semiconnected(G=graph))
    return value


def checkIsAttractingComponent(graph: DiGraph) -> int:
    """


    :param graph: DiGraph:
    :param bar: Bar:

    """
    value: int = int(is_attracting_component(G=graph))
    return value


def checkIsStronglyConnected(graph: DiGraph) -> int:
    """


    :param graph: DiGraph:
    :param bar: Bar:

    """
    value: int = int(is_strongly_connected(G=graph))
    return value


def checkIsWeaklyConnected(graph: DiGraph) -> int:
    """


    :param graph: DiGraph:
    :param bar: Bar:

    """
    value: int = int(is_weakly_connected(G=graph))
    return value


def computeNumberOfWeaklyConnectedComponents(graph: DiGraph) -> int:
    """


    :param graph: DiGraph:
    :param bar: Bar:

    """
    value: int = number_weakly_connected_components(G=graph)
    return value


def computeNumberOfStronglyConnectedComponents(graph: DiGraph) -> int:
    """


    :param graph: DiGraph:
    :param bar: Bar:

    """
    value: int = number_strongly_connected_components(G=graph)
    return value


def computeNumberOfAttracingComponents(graph: DiGraph) -> int:
    """


    :param graph: DiGraph:
    :param bar: Bar:

    """
    value: int = number_attracting_components(G=graph)
    return value
