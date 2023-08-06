from pathlib import Path
from typing import Dict, Text

from rasa.shared.nlu.training_data.training_data import TrainingData

from neuralspace.nlu.converters.base import DataConverter
from neuralspace.nlu.utils import (
    check_directory_and_create_if_not_available,
    map_entities,
)


class RasaConverter(DataConverter):
    def __init__(
        self, language: Text, entity_mapping: Dict[Text, Text], auto_tag_entities: bool
    ):
        self.language = language
        self.entity_mapping = entity_mapping
        self.auto_tag_entities = auto_tag_entities

    def __lookup_converter(self, final_data):
        list_of_lookups = []
        for value in final_data:
            value["entity"] = value.pop("name")
            value["examples"] = value.pop("elements")
            value["language"] = self.language
            value["entityType"] = "lookup"
            list_of_lookups.append(value)
        return list_of_lookups

    def __regex_converter(self, final_data):
        """
        :param language: To specify which language that the entity belongs
        :type final_data: Dictionary of object that contains all the NLU data.
        """
        list_of_regex = []
        tracker_for_dictionary = []
        for value in final_data:
            if value["name"] not in tracker_for_dictionary:
                tracker_for_dictionary.append(value["name"])
                value["entity"] = value.pop("name")
                value["examples"] = [value.pop("pattern")]
                value["language"] = self.language
                value["entityType"] = "regex"
                list_of_regex.append(value)
            else:
                index = tracker_for_dictionary.index(value["name"])
                list_of_regex[index]["examples"].append(value["pattern"])
        return list_of_regex

    def __synonym_converter(self, final_data):
        """
        :param language: To specify which language that the entity belongs
        :type final_data: Dictionary of object that contains all the NLU data.
        """
        list_of_synonyms = []
        tracker_for_dictionary = []
        for value, key in zip(final_data.values(), list(final_data.keys())):
            if value not in tracker_for_dictionary:
                tracker_for_dictionary.append(value)
                list_of_synonyms.append(
                    {
                        "entity": value,
                        "examples": [],
                        "language": self.language,
                        "entityType": "synonym",
                    }
                )

            index = tracker_for_dictionary.index(value)
            list_of_synonyms[index]["examples"].append(key)
        return list_of_synonyms

    @staticmethod
    def __training_data_converter(
        final_data: TrainingData,
    ):
        """
        :type final_data: Dictionary of object that contains all the NLU data.
        """
        list_of_examples = []
        for ex in final_data.nlu_examples:
            list_of_examples.append(ex.as_dict())
        return list_of_examples

    def convert(self, input_path: Text, output_path: Path, type_of_data: Text):
        from rasa.shared.importers.utils import training_data_from_paths

        data = training_data_from_paths([input_path], language=self.language)
        self.training_data = self.__training_data_converter(data)
        self.lookup_data = self.__lookup_converter(data.lookup_tables)
        self.regex_data = self.__regex_converter(data.regex_features)
        self.synonym_data = self.__synonym_converter(data.entity_synonyms)
        if self.entity_mapping is not {} and self.entity_mapping is not None:
            self.training_data = map_entities(self.training_data, self.entity_mapping)
        if self.auto_tag_entities:
            self.training_data = self.auto_tag_pretrained_entities()
        self.give_data_type(type_of_data)
        check_directory_and_create_if_not_available(output_path)
        self.save_converted_data(
            training_data=self.training_data,
            lookup_data=self.lookup_data,
            synonym_data=self.synonym_data,
            regex_data=self.regex_data,
            directory_to_save_files=output_path,
        )
        return True
