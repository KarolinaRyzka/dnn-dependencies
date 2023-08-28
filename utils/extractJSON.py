import json

with open("huggingface.json") as file:
    data = json.load(file)


filteredData = []

for model in data:
    extractData = {
        "ModelName": model.get("ModelName", None),
        "ModelTask": model.get("ModelTask", None),
        "ModelArchitecture": model.get("ModelArchitecture", None),
    }
    filteredData.append(extractData)

filteredJSON = json.dumps(filteredData, indent=2)

with open("huggingfaceData.json", "w") as file:
    file.write(filteredJSON)
