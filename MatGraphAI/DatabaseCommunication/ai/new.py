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
        max_tokens=250,
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
            class onto_name(AnnotationProperty):
                pass

            new_class = types.new_class(y, s_class)
    print(target_onto.name+".owl")
    target_onto.save(target_onto.name+".owl", format="rdfxml")

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
            target_class.onto_name = source_class.name
        except:
            print("Fehler")
    # Copy and create subclasses recursively
    for subclass in source_class.subclasses():
        target_subclass = copy_class_recursive(subclass, target_ontology, source_ontology, api_key, custom_function)
        target_subclass.is_a.append(target_class)

    return target_class

def add_description_to_class(cls, target_ontology, api_key, file):

    try:
        output = json.loads(chat_with_gpt3_5(ONTOLOGY_ASSISTANT_MESSAGES, cls.name, api_key))
        cls.comment = output["description"]
        cls.alternative_labels = str(output["alternative_labels"])
        cls.onto_name = cls.name
    except:
        print("Fehler")
    target_ontology.save(file, format="rdfxml")




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
    file = onto_path[0]+"quantities.owl"
    print(file)
    onto = get_ontology("quantities.owl").load()
    with onto:
        class alternative_labels(AnnotationProperty):
            pass
        class onto_name(AnnotationProperty):
            pass
    for cls in onto.classes():
        if not cls.onto_name:
            add_description_to_class(cls, onto, api_key, file)
        # add_description_to_class(cls, onto, api_key, file)
    # onto = []
    # onto.append(get_ontology("materials.owl").load())
    # onto.append(get_ontology("quantities.owl").load())
    # onto.append(get_ontology("units.owl").load())
    # base_class =[onto[0]["Matter"],onto[1]["Quantity"],onto[2]["Unit"]]
    # new_ontos = [get_ontology("http://www.example.com/new_mat.owl"),
    #              get_ontology("http://www.example.com/new_quant.owl"),
    #              get_ontology("http://www.example.com/new_unit.owl")]
    #
    # for ont, cls, new in zip(onto, base_class, new_ontos):
    #     copy_class_recursive(cls, new, ont, api_key, chat_with_gpt3_5)




if __name__ == '__main__':
    main()
