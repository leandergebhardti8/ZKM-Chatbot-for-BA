import io, json

def addStory(sfileList, intent, intent_confused, filteredData):
    nfoundintent = False
    nfoundintentConfused = False
    for index, line in enumerate(sfileList):
        line = line.replace("\n", "")
        if line.strip().startswith("* %s" % intent):
            look_for_action = True
            offset = 1
            while (look_for_action):
                if (str(sfileList[index+offset]).startswith("- slot") == False):
                    filteredData[i]["story"] = "%s -> %s" % (intent, sfileList[index+offset].replace("\n", "").strip())
                    look_for_action = False
                    nfoundintent = True
        if line.strip().startswith("* %s" % intent_confused):
            look_for_action = True
            offset = 1
            while (look_for_action):
                if (str(sfileList[index+offset]).startswith("- slot") == False):
                    filteredData[i]["intent_prediction"]["story"] = "%s -> %s" % (intent_confused, sfileList[index+offset].replace("\n", "").strip())
                    look_for_action = False
                    nfoundintentConfused = True
        if (nfoundintentConfused and nfoundintent):
            return filteredData
    return filteredData

with io.open("nlu_results/intent_errors.json", encoding="utf-8", mode="r") as file:
    data = json.load(file)
    filteredData =  list(filter(lambda e: e["intent_prediction"]["confidence"] > 0.40, data))

    with io.open("data/stories.md", encoding="utf-8", mode="r") as sfile:
        sfileList = list(sfile.readlines())
        for i, ele in enumerate(filteredData):
            intent = ele["intent"]
            intent_confused = ele["intent_prediction"]["name"]
            filteredData = addStory(sfileList, intent, intent_confused, filteredData)

    filteredData.sort(key=lambda e: e["intent_prediction"]["confidence"], reverse=True)
    newJson = json.dumps(filteredData, indent=4, sort_keys=True, ensure_ascii=False)
    with io.open("nlu_results/intent_errors_mod.json", encoding="utf-8", mode="w") as wfile:
        wfile.write(newJson)