import difflib
import os
from pprint import pprint as print
from typing import List

import networkx as nx
from networkx import DiGraph, read_gexf
from networkx.classes.reportviews import NodeDataView


def listDirectory(folderPath: str):
    """

    :param folderPath: str:
    :param folderPath: str:
    :param folderPath: str:
    :param folderPath: str:
    :param folderPath: str:
    :param folderPath: str:
    :param folderPath: str:

    """
    return os.listdir(path=folderPath)


def subgraphtoTuple(subgraph: DiGraph) -> tuple:
    """

    :param subgraph: DiGraph:
    :param subgraph: DiGraph:
    :param subgraph: DiGraph:
    :param subgraph: DiGraph:
    :param subgraph: DiGraph:
    :param subgraph: DiGraph:
    :param subgraph: DiGraph:

    """
    data: List[str] = []
    nodeOperations: NodeDataView = subgraph.nodes(data="Operation_Type")
    nodeOperationsList: List[tuple[str, str]] = list(nodeOperations)

    pair: tuple[str, str]
    for pair in nodeOperationsList:
        data.append(pair[1])

    data: tuple = tuple(data)
    return data


#
def folderToSubgraph(folderPath: str) -> List[str]:
    """

    :param folderPath: str:
    :param folderPath: str:
    :param folderPath: str:
    :param folderPath: str:
    :param folderPath: str:
    :param folderPath: str:
    :param folderPath: str:

    """
    subgraphPaths: List[str] = []

    subgraphFiles: list = listDirectory(folderPath=folderPath)

    file: str
    for file in subgraphFiles:
        subgraphPaths.append(folderPath + file)

    return subgraphPaths


#
def pathsToDiGraphs(subgraphPaths: List[str]) -> List[DiGraph]:
    """

    :param subgraphPaths: List[str]:
    :param subgraphPaths: List[str]:
    :param subgraphPaths: List[str]:
    :param subgraphPaths: List[str]:
    :param subgraphPaths: List[str]:
    :param subgraphPaths: List[str]:
    :param subgraphPaths: List[str]:

    """
    subgraphs: List[DiGraph] = []

    path: str
    for path in subgraphPaths:
        subgraph: DiGraph = read_gexf(path=path)
        subgraphs.append(subgraph)
    return subgraphs


#
def digraphsToTuples(subgraphs: List[DiGraph]) -> List[tuple]:
    """

    :param subgraphs: List[DiGraph]:
    :param subgraphs: List[DiGraph]:
    :param subgraphs: List[DiGraph]:
    :param subgraphs: List[DiGraph]:
    :param subgraphs: List[DiGraph]:
    :param subgraphs: List[DiGraph]:
    :param subgraphs: List[DiGraph]:

    """
    data: List[tuple] = []

    subgraph: DiGraph
    for subgraph in subgraphs:
        dataTuple: tuple = subgraphtoTuple(subgraph=subgraph)
        data.append(dataTuple)
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
    # model 1
    folderPath1: str = "/Users/karolinaryzka/Documents/dnn-dependencies/dnn_dependencies/subgraphs/bert-base-uncased/"
    subgraphPaths1: List[str] = folderToSubgraph(folderPath=folderPath1)
    subgraphs1 = pathsToDiGraphs(subgraphPaths1)
    data1: List[tuple] = digraphsToTuples(subgraphs1)

    # model 2
    folderPath2: str = "/Users/karolinaryzka/Documents/dnn-dependencies/dnn_dependencies/subgraphs/felflare-bert-restore-punctuation/"
    subgraphPaths2: List[str] = folderToSubgraph(folderPath=folderPath2)
    subgraphs2 = pathsToDiGraphs(subgraphPaths2)
    data2: List[tuple] = digraphsToTuples(subgraphs2)

    comparison(data1, data2)


main()


# results: List[bool] = []
# trueResult: List[tuple, tuple] = []
# pairings = product(model1Data, model2Data)
# i: tuple
# for i in pairings:
#     results.append(i[0] == i[1])
#     if (i[0]==i[1]):
#         countTrue += 1
#         trueResult.append(i)
#     countTotal += 1
# print(countTrue)
# print(countTotal)
# print(f"{(countTrue / countTotal) * 100}%")
