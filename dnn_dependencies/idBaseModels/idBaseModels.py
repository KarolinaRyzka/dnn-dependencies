from pathlib import Path
from typing import List

import click
import pandas
from numpy import NaN
from pandas import DataFrame, Series
from sqlalchemy import Connection, Engine, MetaData

from dnn_dependencies.schemas import sql

COLUMNS: dict[str, str] = {"name": "Model Name", "filepath": "Model Filepath"}


def readDB(dbFile: Path) -> DataFrame:
    dbEngine: Engine = sql.createEngine(path=dbFile.__str__())
    dbConn: Connection = dbEngine.connect()

    df: DataFrame = pandas.read_sql_table(table_name="ModelStats", con=dbConn)

    dbConn.close()

    return df


def createMask(df: DataFrame, column: str) -> Series:
    series: Series = df[column]
    mask: Series = (series.str.find("huggingface.co")) > -1
    return mask


def applyMask(df: DataFrame, mask: Series, column: str) -> DataFrame:
    df.loc[~mask, column] = NaN
    df.dropna(inplace=True)
    return df


def formatDF(df: DataFrame, keepColumns: List[str]) -> DataFrame:
    orderedColumns: List[str] = ["ID"] + keepColumns

    df.drop(
        columns=[column for column in df.columns if column not in keepColumns],
        inplace=True,
    )

    df["ID"] = df.index
    df.reset_index(inplace=True)
    orderedDF: DataFrame = df.reindex(columns=orderedColumns)

    return orderedDF


def writeToDB(df: DataFrame, dbFile: Path) -> None:
    dbMetadata: MetaData = MetaData()

    dbEngine: Engine = sql.createEngine(path=dbFile.__str__())
    dbConn: Connection = dbEngine.connect()

    sql.schema_BaseModels(metadata=dbMetadata)
    sql.createTables(metadata=dbMetadata, engine=dbEngine)

    df.to_sql(name="BaseModels", con=dbConn, if_exists="fail", index=True)

    dbConn.close()


@click.command()
@click.option(
    "dbFile",
    "-i",
    "--input",
    nargs=1,
    type=Path,
    help="Path to database to read from and write to",
)
def main(dbFile: Path) -> None:
    dbFile = dbFile.absolute()

    print(dbFile)

    dbDF: DataFrame = readDB(dbFile=dbFile)
    mask: Series = createMask(df=dbDF, column=COLUMNS["filepath"])
    df: DataFrame = applyMask(df=dbDF, mask=mask, column=COLUMNS["filepath"])

    orderedDF: DataFrame = formatDF(df=df, keepColumns=list(COLUMNS.values()))

    writeToDB(df=orderedDF, dbFile=dbFile)


if __name__ == "__main__":
    main()
