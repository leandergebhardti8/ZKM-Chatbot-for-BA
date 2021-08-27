import logging, io, json
from typing import List, Dict, Any, Optional, Text
import locale
from datetime import datetime
from fuzzywuzzy import fuzz


logger = logging.getLogger(__name__)

ATTR_MAP = "attribute-mapping"
ATTR_KEY_MAP = "attribute-key-mapping"
ENT_MAP = "entity-type-mapping"
MEN_MAP = "mention-mapping"

def equalComp(value1, value2):
    similarity = fuzz.ratio(value1, value2)
    return  similarity > 80

def containsComp(array, value):
    return value in array

def compareDates(dateObject, vdate):
    start = dateObject["start"]
    end = dateObject["end"]
    return (
    datetime.strptime(start[:10], '%Y-%m-%d').date()
    <= datetime.strptime(vdate[:10], '%Y-%m-%d').date()
    and 
    datetime.strptime(end[:10], '%Y-%m-%d').date()
    >= datetime.strptime(vdate[:10], '%Y-%m-%d').date()
    )

indices = {
    "person" : "name",
    "event": "title",
    "creation": "title"
}

class dbNode():
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class JsonDataTree(object):
    instance = None
    # 1 2 3 4 5 6 7
    def buildTree(self, arr):
        if not arr:
            return None
        
        mid = int(len(arr) / 2)
        node = dbNode(arr[mid])
        node.right = self.buildTree(arr[mid+1:])
        node.left = self.buildTree(arr[:mid])
        return node

    @staticmethod
    def get_instance():
        if not JsonDataTree.instance:
            JsonDataTree()
        return JsonDataTree.instance
    
    def __init__(self):
        with io.open("export.json", mode='r', encoding='utf-8') as data:
            jdata = json.load(data)
            dataTree = {}
            for key, value in indices.items():
                jdata[key].sort(key=lambda x: x[value])
                print(len(jdata[key]))
                rootNode =  self.buildTree(jdata[key])
                dataTree[key] = rootNode
            JsonDataTree.instance = dataTree

class JsonData(object):
    instance = None

    @staticmethod
    def get_instance():
        if not JsonData.instance:
            JsonData()
        return JsonData.instance
    
    def __init__(self):
        with io.open("export.json", mode='r', encoding='utf-8') as data:
            jdata = json.load(data)
            JsonData.instance = jdata

JsonData.get_instance()
JsonDataTree.get_instance()

class KnowledgeBase(object):

    def get_entities(
        self,
        entity_type: Text,
        attributes: Optional[List[Dict[Text, Text]]] = None,
        limit: int = 5,
    ) -> List[Dict[Text, Any]]:

        raise NotImplementedError("Method is not implemented.")

    def get_attribute_of(
        self, entity_type: Text, key_attribute: Text, entity: Text, attribute: Text
    ) -> List[Any]:

        raise NotImplementedError("Method is not implemented.")

    def validate_entity(
        self, entity_type, entity, key_attribute, attributes
    ) -> Optional[Dict[Text, Any]]:

        raise NotImplementedError("Method is not implemented.")

    def map(self, mapping_type: Text, mapping_key: Text) -> Text:

        raise NotImplementedError("Method is not implemented.")

class InMemoryGraph(KnowledgeBase):

    def __init__(self):
        self.graph = JsonData.get_instance()
        self.graphTree = JsonDataTree.get_instance()
        
        self.attribute_mapping = {
            "nationality": {
                "Deutschland" : "deutsch",
                "deutschland" : "deutsch",
            },
            "date": {
                "heute" : datetime.now().strftime("%Y-%m-%d"),
                "gerade" : datetime.now().strftime("%Y-%m-%d"),
                "gerade?" : datetime.now().strftime("%Y-%m-%d"),
            }
        }
        # right are the fields from export.json
        self.attribute_key_mapping = {
            "time": "date",
            "nationalität" : "nationality",
            "nationality" : "nationality",
            "biography" : "biography_de",
            "biographie" : "biography_de",
            "eintritt" : "entrancefee",
            "veranstaltungsort" : "location_name",
            "date_start" : "date_start",
            "date_end" : "date_end",
            "category" : "category",
            "subcategory" : "subcategory",
            "creation_date" : "creation_date"
        }
        self.entity_type_mapping = {
            "PER": "person",
            "LOC": "person",
            "MISC": "event",
            "leute": "person",
            "künstlern": "person",
            "künstler": "person",
            "event": "event",
            "programmansicht": "event",
            "programm": "event",
            "vortrag": "event",
            "workshop": "event",
            "Workshop": "event",
            "workshops": "event",
            "Workshops": "event",
            "veranstaltungen": "event",
            "ausstellungen": "event",
            "Ausstellungen": "event",
            "creation" : "creation"
            }

        self.entity_sort_key = {
            'person': None,
            'creation': None,
            'event': lambda event: datetime.strptime(event["date"]["start"][:10], '%Y-%m-%d').date(),
            'publication': None,
            'image': None
        }

        self.mention_mapping = {
            "erste": "0",
            "zweite": "1",
            "dritte": "2",
            "vierte": "3",
            "fünfte": "4",
            "letzte": "-1",
            "1": "1",
            "2": "2",
            "3": "3",
            "4": "4",
            "5": "5",
        }

    def get_entities(
        self,
        entity_type: Text,
        attributes: Optional[List[Dict[Text, Text]]] = None,
        limit: int = 8,
    ) -> List[Dict[Text, Any]]:
        """
        Query the graph database for entities of the given type. Restrict the entities
        by the provided attributes, if any attributes are given.
        :param entity_type: the entity type
        :param attributes: list of attributes
        :param limit: maximum number of entities to return
        :return: list of entities
        """
        if (entity_type == 'Workshops'):
            entity_type = 'workshop'
        if (entity_type == 'Ausstellungen'):
            entity_type = 'ausstellungen'
        if entity_type not in self.graph:
            return []

        entities = self.graph[entity_type]

        # filter entities by attributes
        if attributes:
            entities = list(
                filter(
                    lambda e: [a["comp"](e[a["key"]], a["value"]) for a in attributes].count(
                        False
                    )
                    == 0,
                    entities,
                )
            )
        logger.debug(entities)
        return entities[:limit]

    def get_entities_op(
        self,
        entity_type: Text,
        attributes: Optional[List[Dict[Text, Text]]] = None,
        limit: int = 8,
    ) -> List[Dict[Text, Any]]:
        """
        Query the graph database for entities of the given type. Restrict the entities
        by the provided attributes, if any attributes are given.
        :param entity_type: the entity type
        :param attributes: list of attributes
        :param limit: maximum number of entities to return
        :return: list of entities
        """
        if entity_type not in self.graph:
            return []

        entities = self.graphTree[entity_type]
        a = attributes[0]
        root = entities
        found_entities = []
        while root is not None:
            print("value %s" % (root.value[a["key"]]))
            if a["comp"](root.value[a["key"]], a["value"]):
                found_entities.append(root.value)
                break
            if root.value[a["key"]] > a["value"]:
                root = root.left
                continue
            if root.value[a["key"]] < a["value"]:
                root = root.right
                continue

        return found_entities[:limit]

    def get_entities_corr(
        self,
        entity_type: Text,
        attribute: Text,
        corr_entity_id: int,
        limit: int = 8,
    ) -> List[Dict[Text, Any]]:
        """
        Query the graph database for entities of the given type. Restrict the entities
        by the provided attributes, if any attributes are given.
        :param entity_type: the entity type
        :param attributes: list of attributes
        :param limit: maximum number of entities to return
        :return: list of entities
        """
        if entity_type not in self.graph:
            return []

        entities = self.graph[entity_type]

        # filter entities by attributes
        entities = list(
                filter(
                    lambda e: corr_entity_id in e[attribute],
                    entities,
                )
            )

        return entities[:limit]

    def get_entity_id(
        self,
        entity_type: Text,
        entity_key_value: Text,
        entity_key: Text
    ):
        entities = self.graph[entity_type]

        for entity in entities:
            if (entity[entity_key] == entity_key_value):
                return entity["vid"]
        return None


    def get_attribute_of(
        self, entity_type: Text, key_attribute: Text, entity: Text, attribute: Text
    ) -> List[Any]:
        """
        Get the value of the given attribute for the provided entity.
        :param entity_type: can be Person, event, creation...
        :param key_attribute: attribute by wich the db is gonna be query to.
        :param entity: value of the key attribute to search for.
        :param attribute: attribute of interest.
        :return: the value of the attribute of interest.
        """
        if entity_type not in self.graph:
            return []

        entities = self.graph[entity_type]

        entities_of_interest = list(
            filter(lambda e: equalComp(e[key_attribute], entity), entities)
        )
        
        if self.entity_sort_key[entity_type] is not None:
            entities_of_interest.sort(key=self.entity_sort_key[entity_type], reverse=True)

        if not entities_of_interest:
            return []

        return [entities_of_interest[0][attribute]]

    def validate_entity(
        self, entity_type, entity, key_attribute, attributes
    ) -> Optional[Dict[Text, Any]]:
        """
        Validates if the given entity has all provided attribute values.
        :param entity_type: entity type
        :param entity: name of the entity
        :param key_attribute: key attribute of entity
        :param attributes: attributes
        :return: the found entity
        """
        if entity_type not in self.graph:
            return None

        entities = self.graph[entity_type]

        entity_of_interest = list(
            filter(lambda e: e[key_attribute] == entity, entities)
        )

        if not entity_of_interest or len(entity_of_interest) > 1:
            return None

        entity_of_interest = entity_of_interest[0]

        for a in attributes:
            if entity_of_interest[a["key"]] != a["value"]:
                return None

        return entity_of_interest
    
    def get_attribute_mapping_list(self) -> Dict:
        return self.attribute_mapping


    def map(self, mapping_type: Text, mapping_key: Text, attribute_key: Text = None) -> Text:
        """
        Query the given mapping table for the provided key.
        :param mapping_type: the name of the mapping table
        :param mapping_key: the mapping key
        :return: the mapping value
        """

        if (
            mapping_type == ATTR_MAP
            and attribute_key in self.attribute_mapping
            and mapping_key in self.attribute_mapping[attribute_key]
        ):
            return self.attribute_mapping[attribute_key][mapping_key]

        if (
            mapping_type == ENT_MAP
            and mapping_key in self.entity_type_mapping
        ):
            return self.entity_type_mapping[mapping_key]

        if (
            mapping_type == ATTR_KEY_MAP
            and mapping_key in self.attribute_key_mapping
        ):
            return self.attribute_key_mapping[mapping_key]

        if (
            mapping_type == MEN_MAP
            and mapping_key in self.mention_mapping
        ):
            return self.mention_mapping[mapping_key]
        