# from pprint import pprint as print
from typing import List

import networkx as nx
from networkx import DiGraph, read_gexf
from progress.bar import Bar


def graphToSet(graph: DiGraph) -> set[str]:
    """

    :param graph: DiGraph:
    :param graph: DiGraph:
    :param graph: DiGraph:
    :param graph: DiGraph:
    :param graph: DiGraph:
    :param graph: DiGraph:
    :param graph: DiGraph:

    """
    nodeOps: List[tuple] = list(graph.nodes(data="Operation_Type"))
    graphOps: List[str] = [pair[1] for pair in nodeOps]

    # print(graphOps)
    return set(graphOps)


def jaccardIndex(model1Data: set[str], model2Data: set[str]) -> float:
    """

    :param model1Data: set[str]:
    :param model2Data: set[str]:
    :param model1Data: set[str]:
    :param model2Data: set[str]:
    :param model1Data: set[str]:
    :param model2Data: set[str]:
    :param model1Data: set[str]:
    :param model2Data: set[str]:
    :param model1Data: set[str]:
    :param model2Data: set[str]:
    :param model1Data: set[str]:
    :param model2Data: set[str]:
    :param model1Data: set[str]:
    :param model2Data: set[str]:

    """
    intersection = model1Data.intersection(model2Data)
    jaccardIndex = len(intersection) / (
        len(model1Data) + len(model2Data) - len(intersection)
    )
    return jaccardIndex


def main() -> None:
    """ """
    graph1: nx.DiGraph = read_gexf("bert-base-cased.gexf")
    graph2: nx.DiGraph = read_gexf("bert-base-uncased.gexf")
    model1Data: List[str] = graphToSet(graph1)
    model2Data: List[str] = graphToSet(graph2)
    # list1 = ['hello', 'work', 'please']
    # list2 = ['hello', 'work', 'please']
    print(jaccardIndex(model1Data, model2Data))


main()
