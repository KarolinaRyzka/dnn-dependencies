from os import listdir
from pathlib import Path
from typing import List, Tuple

import pandas
from pandas import DataFrame
from progress.bar import Bar


def listFiles(directory: Path) -> Tuple[List[Path], List[Path]]:
    """

    :param directory: Path:
    :param directory: Path:
    :param directory: Path:
    :param directory: Path:
    :param directory: Path:
    :param directory: Path:
    :param directory: Path:

    """
    files: List[Path] = [Path(directory, f) for f in listdir(path=directory)]

    txtFiles: List[Path] = []
    jsonFiles: List[Path] = []

    file: Path
    for file in files:
        if file.suffix == ".txt":
            txtFiles.append(file)

        if file.suffix == ".json":
            jsonFiles.append(file)

    return (txtFiles, jsonFiles)


def extractDataFromDF(df: DataFrame) -> DataFrame:
    """

    :param df: DataFrame:
    :param df: DataFrame:
    :param df: DataFrame:
    :param df: DataFrame:
    :param df: DataFrame:
    :param df: DataFrame:
    :param df: DataFrame:

    """
    df.drop(
        columns=["id", "LatestGitCommitSHA", "ModelHub", "ModelPaperDOIs"], inplace=True
    )
    df.drop(columns=["ModelOwnerURL", "ModelURL", "ModelOwner"], inplace=True)
    return df


def extractDataFromTXTs(filepaths: List[Path]) -> dict[str, Path]:
    """

    :param filepaths: List[Path]:
    :param filepaths: List[Path]:
    :param filepaths: List[Path]:
    :param filepaths: List[Path]:
    :param filepaths: List[Path]:
    :param filepaths: List[Path]:
    :param filepaths: List[Path]:

    """
    REPLACEMENT_STR: str = (
        "./PTM-Torrent/ptm_torrent/huggingface/data/huggingface/repos/"
    )

    data: dict[str, Path] = {}

    with Bar("Extracting data from .txt files... ", max=len(filepaths)) as bar:
        txtFile: Path
        for txtFile in filepaths:
            with open(txtFile, "r") as file:
                lines: List[str] = file.readlines()
                file.close()

            line: str
            for line in lines:
                rawModelPath: str = line.strip().split(" ")[-1]
                rawModelName: str = rawModelPath.replace(REPLACEMENT_STR, "")

                modelNameList: List[str] = rawModelName.split("/")

                modelName: str
                if len(modelNameList) < 2:
                    modelName = f"huggingface.co/{modelNameList[0]}"
                else:
                    modelName = "/".join(modelNameList[0:2])

                modelPath: Path = Path(REPLACEMENT_STR, modelName)

                data[modelName] = modelPath

            bar.next()
    return data


def createDF(txtData: dict[str, Path], jsonData: DataFrame) -> DataFrame:
    """

    :param txtData: dict[str:
    :param Path: param jsonData: DataFrame:
    :param txtData: dict[str:
    :param Path: param jsonData: DataFrame:
    :param txtData: dict[str:
    :param Path: param jsonData: DataFrame:
    :param txtData: dict[str:
    :param Path: param jsonData: DataFrame:
    :param txtData: dict[str:
    :param Path: param jsonData: DataFrame:
    :param txtData: dict[str:
    :param Path: param jsonData: DataFrame:
    :param txtData: dict[str:
    :param Path]:
    :param jsonData: DataFrame:

    """
    COLUMNS: List[str] = ["name", "path", "task", "arch"]
    df: DataFrame = DataFrame(columns=COLUMNS)

    dfSize: int = jsonData.shape[0]

    with Bar("Creating DF of relevant data... ", max=dfSize) as bar:
        row: Tuple[str, str, str]
        for row in jsonData.itertuples(index=False):
            name: str = row[0]

            if name.__contains__("/") == False:
                name = f"huggingface.co/{name}"

            try:
                path: str = txtData[name].__str__()
            except KeyError:
                bar.next()
                continue

            task: str = row[2]
            arch: str = row[1]

            df.loc[-1] = [name, path, task, arch]
            df.index = df.index + 1
            df.sort_index()

            bar.next()

    df.dropna(subset=["task"], inplace=True)
    return df


def createCommands(df: DataFrame) -> None:
    """

    :param df: DataFrame:
    :param df: DataFrame:
    :param df: DataFrame:
    :param df: DataFrame:
    :param df: DataFrame:
    :param df: DataFrame:
    :param df: DataFrame:

    """
    dfSize: int = df.shape[0]
    cmdList: List[str] = []

    with Bar("Creating a list of commands and saving to file... ", max=dfSize) as bar:
        row: Tuple[str, str, str, str]
        for row in df.itertuples(index=False):
            output: str = row[0].replace("/", "_") + ".onnx"
            # optimum-cli export onnx --model $model --framework pt --atol 1 --monolith $outputDirectory
            cmd: str = f"optimum-cli export --monolith --atol 1 --model {row[1]} --task {row[2]} --output {output}\n"
            cmdList.append(cmd)
            bar.next()

    with open("commands.txt", "w") as cmdFile:
        cmdFile.writelines(cmdList)
        cmdFile.close()


def main() -> None:
    """ """
    DIRECTORY: Path = Path("HF_TextFiles")

    txtFiles, jsonFiles = listFiles(directory=DIRECTORY)

    jsonFile: Path = jsonFiles[0]
    jsonDF: DataFrame = pandas.read_json(path_or_buf=jsonFile)
    jsonDF: DataFrame = extractDataFromDF(df=jsonDF)

    txtData: dict[str, Path] = extractDataFromTXTs(filepaths=txtFiles)

    df: DataFrame = createDF(txtData=txtData, jsonData=jsonDF)

    createCommands(df=df)


if __name__ == "__main__":
    main()
