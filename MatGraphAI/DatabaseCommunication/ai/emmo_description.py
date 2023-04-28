import json
import os
from json import JSONDecodeError

import openai
from django.conf import settings
from dotenv import load_dotenv
from owlready2 import *
from DatabaseCommunication.ai.setupMessages import ONTOLOGY_ASSISTANT_MESSAGES

def convert_alternative_labels(onto):
    onto = os.path.join("../../Ontology/", onto)
    ontology = get_ontology(onto).load()
    # Define the new alternative_label property
    with ontology:
        class alternative_label(DataProperty, FunctionalProperty):
            domain = [Thing]
            range = [str]

    # Iterate over all classes in the ontology
    for cls in ontology.classes():
        # If the class has the 'alternative_labels' property
        if cls.alternative_labels:
            # Retrieve the alternative_labels value, parse it, and remove the property
            alt_labels_str = cls.alternative_labels
            cls.alternative_labels = None

            # Parse the alternative_labels string into a list
            alt_labels_list = list(alt_labels_str)

            # Set the new alternative_label property for each label in the list
            for label in alt_labels_list:
                new_alt_label = alternative_label(label)
                cls.alternative_label.append(new_alt_label)

    ontology.save(onto)



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
