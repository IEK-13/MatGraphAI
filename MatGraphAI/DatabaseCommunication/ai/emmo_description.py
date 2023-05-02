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
import re

def convert_alternative_labels(onto):
    onto_path = os.path.join("/home/mdreger/Documents/MatGraphAI/Ontology/", onto)
    onto_path_alt = os.path.join("/home/mdreger/Documents/MatGraphAI/Ontology/alt_list", onto)
    ontology = get_ontology(onto_path_alt).load()

    # Define the new alternative_label property
    # Define the new alternative_label property
    with ontology:
        class alternative_label(AnnotationProperty):
            domain = [Thing]
            range = [str]

        # Iterate over all classes in the ontology
        for cls in ontology.classes():
            # If the class has the 'alternative_labels' property
            if cls.alternative_labels:
                # Retrieve the alternative_labels value, parse it, and remove the property
                alt_labels = list(cls.alternative_labels[0].replace("[", "").replace("]", "").replace("'", "").split(","))
                cls.alternative_labels = []
                for l in alt_labels:
                    label = l.strip()
                    label = label.join(label.split())
                    label = re.sub(r'\W+', '', label)
                    cls.alternative_label.append(label)  # Make sure to use the newly defined property
                    print(label)
            else:
                print(cls, cls.alternative_label)
            print(cls, cls.alternative_label)  # Use the new property name
    # Use the new property name

        print(onto_path)
        ontology.save(onto_path, format="rdfxml")






class OntologyManager:
    def __init__(self, api_key, ontology_folder = "/home/mdreger/Documents/MatGraphAI/Ontology/"):
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
            self.update_ontology(ontology_file)
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
