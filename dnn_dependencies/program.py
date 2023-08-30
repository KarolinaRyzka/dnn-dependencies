from os import listdir
from pathlib import Path
from typing import Any, List, Tuple

import click
import pandas
from networkx import DiGraph
from pandas import DataFrame
from progress.bar import Bar

from metrics.metrics import *
from schemas.sql import SQL

RANDOM_SEED: int = 42

random.seed(a=RANDOM_SEED, version=2)
numpy.random.seed(seed=RANDOM_SEED)


def createModelsDF(directory: Path) -> DataFrame:
    data: dict[str, List[str]] = {"Model Name": [], "Model Filepath": []}

    filepaths: List[Path] = [
        Path(directory, filepath) for filepath in listdir(path=directory)
    ]

    with Bar("Creating DataFrame of models... ", max=len(filepaths)) as bar:
        filepath: Path
        for filepath in filepaths:
            modelName: str = extractModelNameFromFilepath(filepath=filepath)
            data["Model Name"].append(modelName)
            data["Model Filepath"].append(filepath.__str__())
            bar.next()

    df: DataFrame = DataFrame(data=data)

    return df


def createFileGraphPairs(directory: Path) -> List[Tuple[Path, DiGraph]]:
    data: List[DiGraph] = []

    files: List[Path] = [Path(directory, f) for f in listdir(path=directory)]

    with Bar("Reading files to create DiGraphs... ", max=len(files)) as bar:
        file: Path
        for file in files:
            data.append(read_gexf(file))
            bar.next()

    return list(zip(files, data))


def computeEveryModelProperties(
    fileGraphPairs: List[Tuple[Path, DiGraph]]
) -> DataFrame:
    dfList: List[DataFrame] = []

    with Bar("Computing model properties... ", max=len(fileGraphPairs)) as bar:
        pair: Tuple[Path, DiGraph]
        for pair in fileGraphPairs:
            dfList.append(computeModelProperties(fileGraphPair=pair))
            bar.next()

    return pandas.concat(objs=dfList, ignore_index=True)


def extractModelNameFromFilepath(filepath: Path) -> str:
    name: str = filepath.stem
    splitName: List[str] = name.split("_")
    modelName: str = f"{splitName[0]}/{'_'.join(splitName[1::])}".replace(".onnx", "")

    return modelName


def computeModelProperties(fileGraphPair: Tuple[Path, DiGraph]) -> DataFrame:
    data: dict[str, Any] = {}

    modelFilepath: Path = fileGraphPair[0]
    graph: DiGraph = fileGraphPair[1]

    modelName: str = extractModelNameFromFilepath(filepath=modelFilepath)

    data["Model Name"] = modelName
    data["Model Filepath"] = modelFilepath.__str__()
    data["Is Semiconnected"] = checkIsSemiconnected(graph=graph)
    data["Is Attracting Component"] = checkIsAttractingComponent(graph=graph)
    data["Is Strongly Connected"] = checkIsStronglyConnected(graph=graph)
    data["Is Weakly Connected"] = checkIsWeaklyConnected(graph=graph)
    data["Is Triad"] = checkIsTriad(graph=graph)
    data["Is Regular"] = checkIsRegular(graph=graph)
    data["Is Planar"] = checkIsPlanar(graph=graph)
    data["Is Distance Regular"] = checkIsDistanceRegular(graph=graph)
    data["Is Strongly Regular"] = checkIsStronglyRegular(graph=graph)
    data["Is Bipartite"] = checkIsBipartite(graph=graph)
    data["Is Aperiodic"] = checkIsAperiodic(graph=graph)
    data["Is Directed Acyclic"] = checkIsDirectedAcyclicGraph(graph=graph)
    data["Radius"] = computeRadius(graph=graph)
    data["DAG Longest Path Length"] = computeDAGLongestPathLength(graph=graph)
    data["Number of Isolates"] = computeNumberOfIsolates(graph=graph)
    data["Robins Alexander Clustering"] = computeRobinsAlexanderClustering(graph=graph)
    data["Transitivity"] = computeTransitivity(graph=graph)
    data["Number of Nodes"] = computeNumberOfNodes(graph=graph)
    data["Density"] = computeDensity(graph=graph)
    data["Number of Edges"] = computeNumberOfEdges(graph=graph)
    data["Number of Communities"] = computeNumberOfCommunities(graph=graph)
    data["Degree Assortivity Coefficient"] = computeDegreeAssortativityCoefficient(
        graph=graph
    )
    data[
        "Attribute Assortivity Coefficient"
    ] = computeAttributeAssortativityCoefficient(graph=graph)
    data[
        "Number of Weakly Connected Components"
    ] = computeNumberOfWeaklyConnectedComponents(graph=graph)
    data[
        "Number of Strongly Connected Components"
    ] = computeNumberOfStronglyConnectedComponents(graph=graph)
    data["Number of Attracting Components"] = computeNumberOfAttracingComponents(
        graph=graph
    )
    data["Barycenter"] = computeBarycenter(graph=graph)
    data[
        "Degree Pearson Correlation Coefficient"
    ] = computeDegreePearsonCorrelationCoefficient(graph=graph)

    return DataFrame([data])


@click.command()
@click.option(
    "gexfDirectory",
    "-i",
    "--input",
    type=Path,
    required=True,
    nargs=1,
    help="Path to a directory containing at least one (1) GEXF file",
)
@click.option(
    "dbFile",
    "-o",
    "--output",
    type=Path,
    required=True,
    nargs=1,
    help="Path to SQLite3 database to store data",
)
def main(gexfDirectory: Path, dbFile: Path) -> None:
    """
    Compute graph metrics for GEXF files stored in a directory
    \f

    :param gexfDirectory: Path:
    :param dbFile: Path:

    """
    if dbFile.is_file():
        print("Output database already exists. Exiting program")
        quit(1)

    sql: SQL = SQL(sqliteDBPath=dbFile)

    modelsDF: DataFrame = createModelsDF(directory=gexfDirectory)
    sql.writeDFToDB(
        df=modelsDF,
        tableName="Models",
        keepIndex=True,
        indexColumn="ID",
    )

    fileGraphPairs: List[Tuple[Path, DiGraph]] = createFileGraphPairs(
        directory=gexfDirectory
    )
    df: DataFrame = computeEveryModelProperties(fileGraphPairs=fileGraphPairs)

    sql.writeDFToDB(
        df=df,
        tableName="Model Properties",
        keepIndex=True,
        indexColumn="ID"
    )

    sql.closeConnection()

if __name__ == "__main__":
    main()
