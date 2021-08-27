import pandas as pd
import io
import logging, io, json
import locale
from datetime import date
from datetime import timedelta
from datetime import datetime
import argparse

entities_limit = 15

cmd_parser = argparse.ArgumentParser(description="Generates Nlu data", usage="\npython3 scripts/nlu_gen.py -et person -r name\npython3 scripts/nlu_gen.py -et event -f date -r title\n")
cmd_parser.add_argument('--entity_type', '-et', help="Entity to search for example(person, event...)", default="event")
cmd_parser.add_argument('--templates', '-t', help="path to where the example data are located example scripts/templates", default="scripts/templates")
cmd_parser.add_argument('--filter', '-f', help="filter entities by attribute, example date", default=None)
cmd_parser.add_argument('--representation', '-r', help="Attribute use to fill the blank in the templates, example title of entity", default="title")
cmd_parser.add_argument('--output', '-o', help="file where the results are gonna be outputted, default data/result_nlu", default="data/result_nlu")
args = vars(cmd_parser.parse_args())

entity_type = args["entity_type"]
templates_file = args["templates"]
filter_attr = args["filter"]
req_attr = args["representation"]
output_file = args["output"]

print("""
    Running nlu gen with parameters: 
    entity_type {},
    templates_file path: {},
    filter_attr {},
    req_attr {},
""".format(entity_type, templates_file, filter_attr, req_attr))

result_nlu = []

def compare_dates(v1, v2 = date.today() - timedelta(days=765)):
    return datetime.strptime(v1["start"][:10], '%Y-%m-%d').date() > v2

def get_template_list():
    templateList = []
    templateFile = io.open("{}".format(templates_file),'r', encoding='utf8')
    for rline in templateFile:
        line = rline.replace('\n','')
        templateList.append(line)
    templateFile.close()
    return templateList

with io.open("export.json",mode='r', encoding='utf-8') as data:
    graph = json.load(data)

entities = graph[entity_type]

if filter_attr!=None:
    entities = list(
            filter(
                lambda e: compare_dates(e[f"{filter_attr}"]), #generator will only take entities that are more recent than today
                entities,
            )
        )

templateList = get_template_list()

for e in entities[:entities_limit]:
    for template in templateList:
        result_nlu.append(template.replace('+*', "[{}]({})".format(e[f"{req_attr.strip()}"], entity_type)))

saveObject = {"result_nlu": result_nlu}
df = pd.DataFrame(saveObject)
df.to_csv(output_file, index=False)
