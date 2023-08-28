from collections import defaultdict
from re import Match, search
from typing import List

from networkx import DiGraph, read_gexf, write_gexf
from networkx.classes.reportviews import NodeView
from networkx.drawing.nx_pydot import write_dot
from progress.bar import Bar


def findRelevantNodes(
    graph: DiGraph, pattern: str, attribute: str = "label"
) -> defaultdict[str, List[str]]:
    """

    :param graph: DiGraph:
    :param pattern: str:
    :param attribute: str:  (Default value = "label")
    :param graph: DiGraph:
    :param pattern: str:
    :param attribute: str:  (Default value = "label")
    :param graph: DiGraph:
    :param pattern: str:
    :param attribute: str:  (Default value = "label")
    :param graph: DiGraph:
    :param pattern: str:
    :param attribute: str:  (Default value = "label")
    :param graph: DiGraph:
    :param pattern: str:
    :param attribute: str:  (Default value = "label")
    :param graph: DiGraph:
    :param pattern: str:
    :param attribute: str:  (Default value = "label")
    :param graph: DiGraph:
    :param pattern: str:
    :param attribute: str:  (Default value = "label")

    """
    data: defaultdict = defaultdict(list)

    nodes: NodeView = graph.nodes(data=attribute)

    with Bar(
        f"Finding all relevant nodes (matching regex pattern {pattern})... ",
        max=len(nodes),
    ) as progress:
        node: tuple[str, str]
        for node in nodes:
            idx: str = node[0]
            label: str = node[1]

            try:
                match: Match = search(pattern=pattern, string=label)
            except TypeError:
                progress.next()
                continue

            if match:
                data[match.group(0)].append(idx)

            progress.next()

    return data


def condenseLayers(graph: DiGraph, layerNodes: defaultdict[str, List[str]]) -> DiGraph:
    """

    :param graph: DiGraph:
    :param layerNodes: defaultdict[str:
    :param List: str]]:
    :param graph: DiGraph:
    :param layerNodes: defaultdict[str:
    :param List: str]]:
    :param graph: DiGraph:
    :param layerNodes: defaultdict[str:
    :param List: str]]:
    :param graph: DiGraph:
    :param layerNodes: defaultdict[str:
    :param List: str]]:
    :param graph: DiGraph:
    :param layerNodes: defaultdict[str:
    :param List: str]]:
    :param graph: DiGraph:
    :param layerNodes: defaultdict[str:
    :param List: str]]:
    :param graph: DiGraph:
    :param layerNodes: defaultdict[str:
    :param List[str]]:

    """
    dataKeys: List[str] = list(layerNodes.keys())

    with Bar("Condensing layers... ", max=len(dataKeys)) as progress:
        key: str
        for key in dataKeys:
            condensedLayerNodeLabel: str = f"layer_{key}"
            graph.add_node(node_for_adding=condensedLayerNodeLabel)

            node: str
            for node in layerNodes[key]:
                nodeParentEdges: List[str] = list(graph.predecessors(n=node))
                nodeChildEdges: List[str] = list(graph.successors(n=node))

                layerNodeParentEdges: List[tuple[str, str]] = [
                    (edge, condensedLayerNodeLabel) for edge in nodeParentEdges
                ]
                layerNodeChildEdges: List[tuple[str, str]] = [
                    (edge, condensedLayerNodeLabel) for edge in nodeChildEdges
                ]

                graph.add_edges_from(ebunch_to_add=layerNodeParentEdges)
                graph.add_edges_from(ebunch_to_add=layerNodeChildEdges)

            graph.remove_nodes_from(nodes=layerNodes[key])

            progress.next()

    return graph


def deleteRelevantNodes(
    graph: DiGraph, pattern: str, attribute: str = "label"
) -> DiGraph:
    """

    :param graph: DiGraph:
    :param pattern: str:
    :param attribute: str:  (Default value = "label")
    :param graph: DiGraph:
    :param pattern: str:
    :param attribute: str:  (Default value = "label")
    :param graph: DiGraph:
    :param pattern: str:
    :param attribute: str:  (Default value = "label")
    :param graph: DiGraph:
    :param pattern: str:
    :param attribute: str:  (Default value = "label")
    :param graph: DiGraph:
    :param pattern: str:
    :param attribute: str:  (Default value = "label")
    :param graph: DiGraph:
    :param pattern: str:
    :param attribute: str:  (Default value = "label")
    :param graph: DiGraph:
    :param pattern: str:
    :param attribute: str:  (Default value = "label")

    """
    data: List[str] = []

    nodes: NodeView = graph.nodes(data=attribute)

    with Bar(
        f"Finding all relevant nodes to delete (matching regex pattern {pattern})... ",
        max=len(nodes),
    ) as progress:
        node: tuple[str, str]
        for node in nodes:
            idx: str = node[0]
            label: str = node[1]

            try:
                match: Match = search(pattern=pattern, string=label)
            except TypeError:
                progress.next()
                continue

            if match:
                data.append(idx)

            progress.next()

    graph.remove_nodes_from(nodes=data)

    print(f"Deleted {len(data)} node(s) from the graph")

    return graph


def main() -> None:
    """ """
    graph: DiGraph = read_gexf("roberta-base.gexf")

    layer_LayerNodes: defaultdict[str, List[str]] = findRelevantNodes(
        graph=graph,
        pattern=r"layer\.(\d+)",
    )

    embeddings_LayerNodes: defaultdict[str, List[str]] = findRelevantNodes(
        graph=graph, pattern=r"embeddings"
    )

    cls_LayerNodes: defaultdict[str, List[str]] = findRelevantNodes(
        graph=graph, pattern=r"cls"
    )

    # wt_LayerNodes: defaultdict[str, List[str]] = findRelevantNodes(
    #    graph=graph, pattern=r"wt"
    # )

    # condensedGraph: DiGraph = condenseLayers(
    #     graph=graph, layerNodes=embeddings_LayerNodes
    # )
    condensedGraph: DiGraph = condenseLayers(graph=graph, layerNodes=layer_LayerNodes)
    # condensedGraph: DiGraph = condenseLayers(graph=graph, layerNodes=cls_LayerNodes)
    # condensedGraph: DiGraph = condenseLayers(graph=graph, layerNodes=wt_LayerNodes)

    # root_LayerNodes: defaultdict[str, List[str]] = findRelevantNodes(
    #    graph=graph, pattern=r"\/"
    # )

    #    condensedGraph: DiGraph = condenseLayers(
    #        graph=condensedGraph, layerNodes=root_LayerNodes
    #    )

    # condensedGraph: DiGraph = deleteRelevantNodes(
    #    graph=condensedGraph, pattern="Constant"
    # )

    finalGraph: DiGraph = condensedGraph

    write_gexf(finalGraph, "test.gexf")
    write_dot(finalGraph, "test.dot")


if __name__ == "__main__":
    main()
