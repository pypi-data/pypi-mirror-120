import json
from pathlib import Path
from typing import Dict, Text

from neuralspace.nlu.converters.base import DataConverter
from neuralspace.nlu.utils import (
    check_directory_and_create_if_not_available,
    map_entities,
)


class DialogflowConverter(DataConverter):
    def __init__(
        self, language: Text, entity_mapping: Dict[Text, Text], auto_tag_entities: bool
    ):
        self.language = language
        self.entity_mapping = entity_mapping
        self.auto_tag_entities = auto_tag_entities

    @staticmethod
    def __training_data_converter(final_data):
        """
        :type final_data: Dictionary of object that contains all the NLU data.
        """
        list_of_examples = []
        for value in final_data["common_examples"]:
            list_of_examples.append(value)
        return list_of_examples

    def __regex_converter(self, final_data):
        """
        :type final_data: Dictionary of object that contains all the NLU data.
        """
        tracker_for_dictionary = []
        regex_entity = []
        for value in final_data["regex_features"]:
            if value["name"] not in tracker_for_dictionary:
                tracker_for_dictionary.append(value["name"])
                regex_entity.append(
                    {
                        "entity": value["name"],
                        "examples": [],
                        "language": self.language,
                        "entityType": "regex",
                    }
                )
            index = tracker_for_dictionary.index(value["name"])
            regex_entity[index]["examples"].append(value["pattern"])
        return regex_entity

    def __lookup_converter(self, final_data):
        """
        :type final_data: Dictionary of object that contains all the NLU data.
        """
        list_of_lookup = []
        for value in final_data["lookup_tables"]:
            value["entity"] = value.pop("name")
            value["examples"] = value.pop("elements")
            value["language"] = self.language
            value["entityType"] = "lookup"
            list_of_lookup.append(value)

        return list_of_lookup

    def __synonym_converter(self, final_data):
        """
        :type final_data: Dictionary of object that contains all the NLU data.
        """
        list_of_synonyms = []
        for value in final_data["entity_synonyms"]:
            value["entity"] = value.pop("value")
            value["examples"] = value.pop("synonyms")
            value["language"] = self.language
            value["entityType"] = "synonym"
            list_of_synonyms.append(value)
        return list_of_synonyms

    def convert(self, input_path: Text, output_path: Path, type_of_data: Text):
        from rasa.nlu.convert import convert_training_data

        convert_training_data(input_path, "./nlu.json", "json", language=self.language)
        with open("./nlu.json") as f:
            data = json.load(f)["rasa_nlu_data"]
        self.lookup_data = self.__lookup_converter(data)
        self.regex_data = self.__regex_converter(data)
        self.synonym_data = self.__synonym_converter(data)
        self.training_data = self.__training_data_converter(data)
        if self.entity_mapping is not {} and self.entity_mapping is not None:
            self.training_data = map_entities(self.training_data, self.entity_mapping)
        if self.auto_tag_entities:
            self.auto_tag_pretrained_entities()
        self.give_data_type(type_of_data)
        check_directory_and_create_if_not_available(output_path)
        self.save_converted_data(
            training_data=self.training_data,
            lookup_data=self.lookup_data,
            synonym_data=self.synonym_data,
            regex_data=self.regex_data,
            directory_to_save_files=output_path,
        )
