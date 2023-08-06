import os

from rich.console import Console

from neuralspace.constants import ENTITIES, ENTITY, ENTITY_TYPE, PRE_TRAINED

console = Console()


def convert_files(convert, rasa_data):
    lookup_data = convert.lookup_converter(rasa_data.lookup_tables)
    regex_data = convert.regex_converter(rasa_data.regex_features)
    synonym_data = convert.synonym_converter(rasa_data.entity_synonyms)
    training_data = convert.training_data_converter(rasa_data)
    return lookup_data, regex_data, synonym_data, training_data


def check_directory_and_create_if_not_available(directory_to_save_files):
    if not os.path.isdir(directory_to_save_files):
        os.mkdir(directory_to_save_files)


def map_entities(training_data, entities_given):
    for example_index, examples in enumerate(training_data):
        if ENTITIES in list(examples.keys()):
            if examples[ENTITIES] is not []:
                for entity_index, entities in enumerate(examples[ENTITIES]):
                    if entities[ENTITY] in list(entities_given.keys()):
                        training_data[example_index][ENTITIES][entity_index][
                            ENTITY
                        ] = entities_given[
                            training_data[example_index][ENTITIES][entity_index][ENTITY]
                        ]
                        training_data[example_index][ENTITIES][entity_index][
                            ENTITY_TYPE
                        ] = PRE_TRAINED
    return training_data
