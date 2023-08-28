from pathlib import Path

import click
from networkx import Graph, read_gexf
from networkx.drawing.nx_pydot import write_dot


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
    Read in a GEXF file and output the DOT representation of it
    \f

    :param gexfFile: Path: 
    :param dotFile: Path: 

    """
    graph: Graph = read_gexf(gexfFile)
    write_dot(graph, dotFile)


if __name__ == "__main__":
    main()
