import asyncio
import json
import os
from typing import Any, Dict, List, Text

from neuralspace.apis import get_async_http_session
from neuralspace.constants import ENTITIES, ENTITY, ENTITY_TYPE, PRE_TRAINED, TYPE
from neuralspace.nlu.apis import get_entity_list_for_cli


class DataConverter:
    def __init__(self):
        self.training_data = []
        self.lookup_data = []
        self.regex_data = []
        self.synonym_data = []

    @staticmethod
    def __training_data_converter(final_data) -> List[Dict]:
        NotImplementedError("Training data converter is not implemented")
        pass

    def __regex_converter(self, final_data: Dict[Text, Any]) -> List[Dict]:
        NotImplementedError("Regex converter is not implemented")

    def __synonym_converter(self, final_data: Dict[Text, Any]) -> List[Dict]:
        NotImplementedError("synonym converter is not implemented")

    def __lookup_converter(self, final_data: Dict[Text, Any]) -> List[Dict]:
        NotImplementedError("lookup converter is not implemented")

    def convert(self, data):
        NotImplementedError("lookup converter is not implemented")

    @staticmethod
    def save_converted_data(
        lookup_data=None,
        regex_data=None,
        synonym_data=None,
        training_data=None,
        directory_to_save_files=None,
    ):
        if lookup_data is not None:
            with open(os.path.join(directory_to_save_files, "lookup.json"), "w") as f:
                json.dump(lookup_data, f, indent=4)
        if regex_data is not None:
            with open(os.path.join(directory_to_save_files, "regex.json"), "w") as f:
                json.dump(regex_data, f, indent=4)
        if synonym_data is not None:
            with open(os.path.join(directory_to_save_files, "synonym.json"), "w") as f:
                json.dump(synonym_data, f, indent=4)
        if training_data is not None:
            with open(os.path.join(directory_to_save_files, "nlu.json"), "w") as f:
                json.dump(training_data, f, indent=4)

    def auto_tag_pretrained_entities(self):
        loop = asyncio.new_event_loop()
        count_of_entities = loop.run_until_complete(
            get_entity_list_for_cli(entity_type="pre-trained", language=self.language)
        )
        entities_supported = loop.run_until_complete(
            get_entity_list_for_cli(
                entity_type="pre-trained",
                language=self.language,
                count=count_of_entities,
            )
        )
        loop.run_until_complete(get_async_http_session().close())
        for example_index, examples in enumerate(self.training_data):
            if ENTITIES in list(examples.keys()):
                if examples[ENTITIES] is not []:
                    for entity_index, entities in enumerate(examples[ENTITIES]):
                        if entities[ENTITY] in entities_supported:
                            self.training_data[example_index][ENTITIES][entity_index][
                                ENTITY_TYPE
                            ] = PRE_TRAINED
        return self.training_data

    def give_data_type(self, data_type):
        for data_index, _ in enumerate(self.training_data):
            self.training_data[data_index][TYPE] = data_type
