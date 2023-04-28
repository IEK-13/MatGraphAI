import json
import os
from json import JSONDecodeError

import openai
from django.conf import settings
from dotenv import load_dotenv
from owlready2 import *
from DatabaseCommunication.ai.setupMessages import ONTOLOGY_ASSISTANT_MESSAGES

from owlready2 import get_ontology, DataProperty, FunctionalProperty, ObjectProperty, Thing
import os

def convert_alternative_labels(onto):
    onto_path = os.path.join("../../Ontology/", onto)
    ontology = get_ontology(onto_path).load()

    # Define the new alternative_label property
    with ontology:
        class alternative_label(DataProperty, FunctionalProperty):
            range = [str]

        class is_alternative_label(ObjectProperty):
            range = [Thing]

    # Iterate over all classes in the ontology
    for cls in ontology.classes():
        # If the class has the 'alternative_labels' property
        if hasattr(cls, 'alternative_labels') and cls.alternative_labels:
            # Retrieve the alternative_labels value, parse it, and remove the property
            alt_labels_str = cls.alternative_labels
            cls.alternative_labels = None

            # Parse the alternative_labels string into a list
            alt_labels_list = eval(alt_labels_str)

            # Set the new alternative_label property for each label in the list
            for label in alt_labels_list:
                # Create a new class for each alternative label
                new_alt_label_class_name = label.replace(' ', '_')
                new_alt_label_class = ontology.create_class(iri=ontology.base_iri + new_alt_label_class_name)

                # Set the new alternative_label property for the new class
                new_alt_label_class.alternative_label.append(label)

                # Connect the original class with the new alternative_label class using is_alternative_label property
                cls.is_alternative_label.append(new_alt_label_class)

    ontology.save(onto_path)




class OntologyManager:
    def __init__(self, api_key, ontology_folder = "../../Ontology/safe"):
        self.api_key = api_key
        self.ontology_folder = ontology_folder

    def chat_with_gpt3_5(self, setup_message=[], prompt=''):
        openai.api_key = self.api_key

        conversation_history = setup_message
        conversation_history.append({"role": "user", "content": prompt})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation_history,
            max_tokens=250,
            n=1,
            stop=None,
            temperature=0,
        )
        return response["choices"][0]["message"]["content"]
    def update_ontology(self, ontology_file):
        ontology_path = os.path.join(self.ontology_folder, ontology_file)
        onto = get_ontology(ontology_path).load()

        with onto:
            class alternative_labels(AnnotationProperty):
                pass
            class onto_name(AnnotationProperty):
                pass

        for cls in onto.classes():
            if not cls.onto_name:
                print(cls.name)
                try:
                    output = self.chat_with_gpt3_5(ONTOLOGY_ASSISTANT_MESSAGES, cls.name)
                    print(output)
                    output = json.loads(output)
                    cls.comment = output["description"]
                    cls.alternative_labels = str(output["alternative_labels"])
                    cls.onto_name = cls.name
                except JSONDecodeError:
                    print(f"Invalid JSON response for class: {cls.name}")

        onto.save(ontology_path, format="rdfxml")

    def update_all_ontologies(self):
        ontologies = [f for f in os.listdir(self.ontology_folder) if f.endswith(".owl")]

        for ontology_file in ontologies:
            # self.update_ontology(ontology_file)
            convert_alternative_labels(ontology_file)



def main():
    # Get the project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Change the current working directory to the project root directory
    os.chdir(project_root)

    load_dotenv()

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Mat2DevPlatform.settings")
    api_key = settings.OPENAI_API_KEY
    ontology_folder = "/home/mdreger/Documents/MatGraphAI/Ontology/"

    ontology_manager = OntologyManager(api_key, ontology_folder)
    ontology_manager.update_all_ontologies()


if __name__ == "__main__":
    main()
