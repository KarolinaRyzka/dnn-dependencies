from concurrent.futures import ThreadPoolExecutor
from typing import List

from networkx import DiGraph, read_gexf
from networkx.classes.reportviews import NodeDataView, NodeView, OutEdgeView
from progress.bar import Bar

subgraphList: List[DiGraph] = []


def _addNodesToSubgraph(
    subgraph: DiGraph,
    headGraphNodes: NodeDataView | NodeView,
    subgraphNodes: List[str],
) -> None:
    """

    :param subgraph: DiGraph:
    :param headGraphNodes: NodeDataView | NodeView:
    :param subgraphNodes: List[str]:
    :param subgraph: DiGraph:
    :param headGraphNodes: NodeDataView | NodeView:
    :param subgraphNodes: List[str]:
    :param subgraph: DiGraph:
    :param headGraphNodes: NodeDataView | NodeView:
    :param subgraphNodes: List[str]:
    :param subgraph: DiGraph:
    :param headGraphNodes: NodeDataView | NodeView:
    :param subgraphNodes: List[str]:
    :param subgraph: DiGraph:
    :param headGraphNodes: NodeDataView | NodeView:
    :param subgraphNodes: List[str]:
    :param subgraph: DiGraph:
    :param headGraphNodes: NodeDataView | NodeView:
    :param subgraphNodes: List[str]:
    :param subgraph: DiGraph:
    :param headGraphNodes: NodeDataView | NodeView:
    :param subgraphNodes: List[str]:

    """
    node: str
    for node in subgraphNodes:
        subgraph.add_node(node, **headGraphNodes[node])

    return subgraph


def _addEdgesToSubgraph(
    subgraph: DiGraph,
    edgeData: OutEdgeView,
    subgraphNodes: List[str],
) -> DiGraph:
    """

    :param subgraph: DiGraph:
    :param edgeData: OutEdgeView:
    :param subgraphNodes: List[str]:
    :param subgraph: DiGraph:
    :param edgeData: OutEdgeView:
    :param subgraphNodes: List[str]:
    :param subgraph: DiGraph:
    :param edgeData: OutEdgeView:
    :param subgraphNodes: List[str]:
    :param subgraph: DiGraph:
    :param edgeData: OutEdgeView:
    :param subgraphNodes: List[str]:
    :param subgraph: DiGraph:
    :param edgeData: OutEdgeView:
    :param subgraphNodes: List[str]:
    :param subgraph: DiGraph:
    :param edgeData: OutEdgeView:
    :param subgraphNodes: List[str]:
    :param subgraph: DiGraph:
    :param edgeData: OutEdgeView:
    :param subgraphNodes: List[str]:

    """
    u: str
    v: str
    edgeAttributes: dict

    for u, v, edgeAttributes in edgeData:
        if u in subgraphNodes and v in subgraphNodes:
            subgraph.add_edge(u, v, **edgeAttributes)

    return subgraph


def createSubgraph(
    headGraphNodes: NodeDataView | NodeView,
    headGraphEdgeData: OutEdgeView,
    subgraphNodes: List[str],
) -> DiGraph:
    """

    :param headGraphNodes: NodeDataView | NodeView:
    :param headGraphEdgeData: OutEdgeView:
    :param subgraphNodes: List[str]:
    :param headGraphNodes: NodeDataView | NodeView:
    :param headGraphEdgeData: OutEdgeView:
    :param subgraphNodes: List[str]:
    :param headGraphNodes: NodeDataView | NodeView:
    :param headGraphEdgeData: OutEdgeView:
    :param subgraphNodes: List[str]:
    :param headGraphNodes: NodeDataView | NodeView:
    :param headGraphEdgeData: OutEdgeView:
    :param subgraphNodes: List[str]:
    :param headGraphNodes: NodeDataView | NodeView:
    :param headGraphEdgeData: OutEdgeView:
    :param subgraphNodes: List[str]:
    :param headGraphNodes: NodeDataView | NodeView:
    :param headGraphEdgeData: OutEdgeView:
    :param subgraphNodes: List[str]:
    :param headGraphNodes: NodeDataView | NodeView:
    :param headGraphEdgeData: OutEdgeView:
    :param subgraphNodes: List[str]:

    """
    subgraph: DiGraph = DiGraph()

    _addNodesToSubgraph(
        subgraph=subgraph,
        headGraphNodes=headGraphNodes,
        subgraphNodes=subgraphNodes,
    )
    _addEdgesToSubgraph(
        subgraph=subgraph,
        edgeData=headGraphEdgeData,
        subgraphNodes=subgraphNodes,
    )

    return subgraph


def main() -> None:
    """ """
    graph: DiGraph = read_gexf("bert-base-cased.gexf")

    nodes: NodeDataView | NodeView = graph.nodes()
    edgeData: OutEdgeView = graph.edges.data()

    with Bar("Computing all possible subgraphs... ", max=len(nodes)) as progress:

        def _run(headGraphNodes: NodeDataView | NodeView) -> None:
            """

            :param headGraphNodes: NodeDataView | NodeView:
            :param headGraphNodes: NodeDataView | NodeView:
            :param headGraphNodes: NodeDataView | NodeView:
            :param headGraphNodes: NodeDataView | NodeView:
            :param headGraphNodes: NodeDataView | NodeView:
            :param headGraphNodes: NodeDataView | NodeView:
            :param headGraphNodes: NodeDataView | NodeView:

            """
            subgraph: DiGraph = DiGraph()

            nodeList: List = list(headGraphNodes)

            tortiseNode: str
            hareNode: str

            for tortiseNode in headGraphNodes:
                foo: int = int(tortiseNode)

                for hareNode in headGraphNodes:
                    bar: int = int(hareNode)

                    if foo > bar:
                        continue

                    subgraph: DiGraph = DiGraph()
                    subgraphNodes: List[str] = nodeList[foo:bar]

                    _addNodesToSubgraph(
                        subgraph=subgraph,
                        headGraphNodes=headGraphNodes,
                        subgraphNodes=subgraphNodes,
                    )

                    subgraphList.append(subgraph)
            progress.next()

        with ThreadPoolExecutor(max_workers=4) as executor:
            executor.map(_run, nodes)

        print(len(subgraphList))


if __name__ == "__main__":
    main()
