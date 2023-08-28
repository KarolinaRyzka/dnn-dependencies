from pathlib import Path
from typing import Literal

from pandas import DataFrame
from sqlalchemy import (Column, Connection, Engine, Float, ForeignKey, Integer,
                        MetaData, String, Table, create_engine)


class SQL:
    def __init__(self, sqliteDBPath: Path) -> None:
        sqliteURI: str = f"sqlite:///{sqliteDBPath.absolute().__str__()}"

        self.modelsTableName: str = "Models"
        self.baseModelsTableName: str = "Base Models"
        self.modelPropertiesTableName: str = "Model Properties"

        self.metadata: MetaData = MetaData()

        self.engine: Engine = create_engine(url=sqliteURI)
        self.conn: Connection = self.engine.connect()

    def closeConnection(self) -> bool:
        self.conn.close()
        return self.conn.closed

    def createSchema_Models(self) -> None:
        Table(
            self.modelsTableName,
            self.metadata,
            Column(
                name="ID",
                type_=Integer,
                primary_key=True,
                unique=True,
                autoincrement=True,
            ),
            Column(name="Model Name", type_=String),
            Column(name="Model Filepath", type_=String),
        )

    def createSchema_BaseModels(self) -> None:
        Table(
            self.baseModelsTableName,
            self.metadata,
            Column(
                "ID",
                Integer,
                primary_key=True,
                unique=True,
                autoincrement=True,
            ),
            Column(
                "Model ID",
                Integer,
                ForeignKey(f"{self.modelsTableName}.ID"),
                unique=True,
            ),
        )

    def createSchema_ModelProperties(self) -> None:
        Table(
            self.modelPropertiesTableName,
            self.metadata,
            Column(
                "ID",
                Integer,
                primary_key=True,
                unique=True,
                autoincrement=True,
            ),
            Column("Model Name", String),
            Column("Model Filepath", String),
            Column("Is Semiconnected", String),
            Column("Is Attracting Component", String),
            Column("Is Strongly Connected", Integer),
            Column("Is Weakly Connected", Integer),
            Column("Is Triad", Integer),
            Column("Is Regular", Integer),
            Column("Is Planar", Integer),
            Column("Is Distance Regular", Integer),
            Column("Is Strongly Regular", Integer),
            Column("Is Bipartite", Integer),
            Column("Is Aperiodic", Integer),
            Column("Is Directed Acyclic", Integer),
            Column("Radius", Integer),
            Column("DAG Longest Path Length", Integer),
            Column("Number of Isolates", Integer),
            Column("Robins Alexander Clustering", Float),
            Column("Transitivity", Float),
            Column("Number of Nodes", Integer),
            Column("Density", Float),
            Column("Number of Edges", Integer),
            Column("Number of Communities", Integer),
            Column("Degree Assortivity Coefficient", Float),
            Column("Attribute Assortivity Coefficient", Float),
            Column("Number of Weakly Connected Components", Integer),
            Column("Number of Strongly Connected Components", Integer),
            Column("Number of Attracting Components", Integer),
            Column("Barycenter", Integer),
            Column("Degree Pearson Correlation Coefficient", Float),
        )

    def createTables(self) -> None:
        self.metadata.create_all(bind=self.conn)

    def writeDFToDB(
        self,
        df: DataFrame,
        tableName: Literal["Models", "Base Models", "Model Properties"],
        keepIndex: bool,
        indexColumn: str | None = None,
    ) -> None:
        df.to_sql(
            name=tableName,
            con=self.conn,
            if_exists="fail",
            index=keepIndex,
            index_label=indexColumn,
        )
