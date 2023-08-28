from itertools import pairwise
from pathlib import Path
from typing import List

import click
from bs4 import BeautifulSoup, ResultSet, Tag
from networkx import DiGraph
from networkx.drawing.nx_pydot import write_dot
from progress.bar import Bar


def extractNodeLabels(dom: str) -> List[str]:
    """


    :param dom: str:

    """
    data: List[str] = []

    soup: BeautifulSoup = BeautifulSoup(markup=dom, features="xml")
    nodeTags: ResultSet = soup.findAll(name="node")

    with Bar("Extacting node labels... ", max=len(nodeTags)) as bar:
        tag: Tag
        for tag in nodeTags:
            data.append(str(tag.get(key="label")))
            bar.next()

    return data


def buildEdgeList(labels: List[str]) -> List[tuple[str, str]]:
    """


    :param labels: List[str]:

    """
    data: List[tuple[str, str]] = []

    rootTag: str = "onnxComputationalGraph"

    with Bar("Creating edge list... ", max=len(labels)) as bar:
        label: str
        for label in labels:
            nodeList: List[str] = [rootTag]
            splitLabel: List[str] = label.split(sep="/")

            if len(splitLabel) > 1:
                foo: str = rootTag + label
                nodeList = foo.split(sep="/")
            else:
                nodeList.append(splitLabel[0])

            edgeList: List[tuple[str, str]] = list(pairwise(nodeList))
            data.extend(edgeList)

            bar.next()
    return data


def buildDiGraph(edgeList: List[tuple[str, str]]) -> DiGraph:
    """


    :param edgeList: List[tuple[str:
    :param str]]:

    """
    graph: DiGraph = DiGraph()
    graph.add_edges_from(ebunch_to_add=edgeList)
    return graph


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
    "dotFile",
    "-o",
    "--output",
    type=Path,
    required=True,
    nargs=1,
    help="Path to store DOT file",
)
def main(gexfFile: Path, dotFile: Path) -> None:
    """
    Visualize node labels and their edges
    \f

    :param gexfFile: Path:
    :param dotFile: Path:

    """
    with open(file=gexfFile, mode="r") as xmlDoc:
        xmlDOM: str = xmlDoc.read()
        xmlDoc.close()

    nodeLabels: List[str] = extractNodeLabels(dom=xmlDOM)
    edgeList: List[tuple[str, str]] = buildEdgeList(labels=nodeLabels)
    graph: DiGraph = buildDiGraph(edgeList=edgeList)
    write_dot(graph, dotFile)


if __name__ == "__main__":
    main()
