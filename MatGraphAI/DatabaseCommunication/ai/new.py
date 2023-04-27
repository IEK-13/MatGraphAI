import json

import openai
from django.conf import settings
from dotenv import load_dotenv
from owlready2 import *

from DatabaseCommunication.ai.setupMessages import ONTOLOGY_ASSISTANT_MESSAGES


def chat_with_gpt3_5(setup_message=[], prompt='', api_key=''):
    openai.api_key = api_key

    conversation_history = setup_message
    conversation_history.append({"role": "user", "content": prompt})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation_history,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0,
    )
    print(response["choices"][0]["message"]["content"])
    return response["choices"][0]["message"]["content"]


def create_new_class(create_class, s_class, target_onto):
    y = create_class
    s_class = tuple(s_class)

    with target_onto:
            class alternative_labels(AnnotationProperty):
                pass
            class name(AnnotationProperty):
                pass

            new_class = types.new_class(y, s_class)

    return new_class


def copy_class_recursive(source_class, target_ontology, source_ontology, api_key, custom_function):
    target_class = target_ontology[source_class.name]

    if target_class is None:
        print("hioer")
        # Create the new class in the target ontology
        parent_classes = source_class.is_a
        target_class = create_new_class(source_class.name, parent_classes, target_ontology)
        # Call the custom function and store the output as an attribute of the class
        try:
            custom_function_output = json.loads(custom_function(ONTOLOGY_ASSISTANT_MESSAGES, source_class.name, api_key))
            target_class.comment = custom_function_output["description"]
            target_class.alternative_labels = str(custom_function_output["alternative_labels"])
            target_class.name = source_class.name
        except:
            print("Fehler")
    # Copy and create subclasses recursively
    for subclass in source_class.subclasses():
        # target_subclass = copy_class_recursive(subclass, target_ontology, source_ontology, api_key, custom_function)
        # target_subclass.is_a.append(target_class)
        pass
    return target_class


def main():
    # print(chat_with_gpt3_5(SETUP_MESSAGES, "LAB6")[0])
    # Get the project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Change the current working directory to the project root directory
    os.chdir(project_root)

    load_dotenv()

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Mat2DevPlatform.settings")
    api_key = settings.OPENAI_API_KEY
    onto_path.append("/home/mdreger/Documents/MatGraphAI/Ontology/")
    onto = get_ontology("manufacturing1.owl").load()

    starting_class = onto["Process"]
    print(list(onto.classes()))
    new_onto = get_ontology("http://www.example.com/new_ontology.owl")
    root_class = copy_class_recursive(starting_class, new_onto, onto, api_key, custom_function=chat_with_gpt3_5)

    # Save the modified ontology to your file system
    new_onto.save("./new_ontology.owl", format="rdfxml")


if __name__ == '__main__':
    main()
