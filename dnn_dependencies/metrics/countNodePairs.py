from collections import defaultdict
from pathlib import Path
from typing import Generator, List, Tuple

import click
from networkx import DiGraph, read_gexf
from networkx.classes.graph import NodeView
from pandas import DataFrame


def extractNodeChildren(graph: DiGraph) -> List[Tuple[str, Generator]]:
    """


    :param graph: DiGraph:

    """
    nodePairs: List[Tuple[str, Generator]] = []
    nodes: NodeView = graph.nodes

    node: str
    for node in nodes:
        children: Generator = graph.successors(n=node)
        nodePairs.append((node, children))
    return nodePairs


def generateHistogramOfNodePairs(
    graph: DiGraph, pairs: List[Tuple[str, Generator]]
) -> defaultdict[Tuple[str, str], int]:
    """


    :param graph: DiGraph:
    :param pairs: List[Tuple[str:
    :param Generator]]:

    """
    data: defaultdict[Tuple[str, str], int] = defaultdict(int)

    nodes: NodeView = graph.nodes

    pair: Tuple[str, Generator]
    for pair in pairs:
        parentID: str = pair[0]
        childrenIDs: Generator = pair[1]

        parentLabel: str = nodes[parentID]["label"]
        parentLabel: str = parentLabel.rsplit("/", 1)[-1].split("_", 1)[0]

        childrenLabels: List[str] = [nodes[childID]["label"] for childID in childrenIDs]
        childrenLabels: List[str] = [
            childLabel.rsplit("/", 1)[-1].split("_", 1)[0]
            for childLabel in childrenLabels
        ]

        childLabel: str
        for childLabel in childrenLabels:
            data[str((parentLabel, childLabel))] += 1

    return data


@click.command()
@click.option(
    "gexfFile",
    "-i",
    "--input",
    type=Path,
    required=True,
    nargs=1,
    help="Path to GEXF file",
)
@click.option(
    "jsonFile",
    "-o",
    "--output",
    type=Path,
    required=True,
    nargs=1,
    help="Path to store JSON file",
)
def main(gexfFile: Path, jsonFile: Path) -> None:
    """
    Count the number of operation type pairings in a GEXF file
    \f

    :param gexfFile: Path:
    :param jsonFile: Path:

    """
    graph: DiGraph = read_gexf(gexfFile)
    nodeChildren: List[Tuple[str, Generator]] = extractNodeChildren(graph=graph)

    histogram: defaultdict[Tuple[str, str], int] = generateHistogramOfNodePairs(
        graph=graph, pairs=nodeChildren
    )

    df: DataFrame = DataFrame().from_dict(data=histogram, orient="index")
    df.reset_index(inplace=True)
    df.columns = ["Node Type Pairs", "Count"]
    df.sort_values(by="Count", inplace=True, ignore_index=True)

    df.T.to_json(path_or_buf=jsonFile, indent=4)


if __name__ == "__main__":
    main()
