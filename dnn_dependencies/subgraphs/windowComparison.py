# from pprint import pprint as print
import difflib
import time
from typing import List

import networkx as nx
from networkx import DiGraph, read_gexf
from networkx.classes.reportviews import NodeDataView
from progress.bar import Bar


def graphToTuples(graph: DiGraph) -> list[tuple]:
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
    data: List[tuple] = []
    idx: int
    step: int = 2
    with Bar("iterating", max=len(graphOps)) as bar:
        while step < len(graphOps):
            for idx in range(len(graphOps)):
                pair: list[str] = graphOps[idx : idx + step]
                data.append(tuple(pair))
            step += 1
            bar.next()
    return data


def comparison(model1Data: List[tuple], model2Data: List[tuple]) -> List[bool]:
    """

    :param model1Data: List[tuple]:
    :param model2Data: List[tuple]:
    :param model1Data: List[tuple]:
    :param model2Data: List[tuple]:
    :param model1Data: List[tuple]:
    :param model2Data: List[tuple]:
    :param model1Data: List[tuple]:
    :param model2Data: List[tuple]:
    :param model1Data: List[tuple]:
    :param model2Data: List[tuple]:
    :param model1Data: List[tuple]:
    :param model2Data: List[tuple]:
    :param model1Data: List[tuple]:
    :param model2Data: List[tuple]:

    """
    result = difflib.SequenceMatcher(None, model1Data, model2Data)
    percent = result.ratio()
    print(percent)
    return percent


def main() -> None:
    """ """
    tic = time.perf_counter
    graph1: nx.DiGraph = read_gexf("bert-base-cased.gexf")
    graph2: nx.DiGraph = read_gexf("gpt2.gexf")
    list1: list[tuple] = graphToTuples(graph1)
    list2: list[tuple] = graphToTuples(graph2)
    comparison(list1, list2)
    toc = time.perf_counter
    print(tic - toc)


main()
