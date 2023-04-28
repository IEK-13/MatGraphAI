from dotenv import load_dotenv
import os
import sys
from preprocess_text import preprocess
from owlready2 import *
# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from new import chat_with_gpt3_5, add_description_to_class
from setupMessages import ONTOLOGY_ASSISTANT_MESSAGES
# Change the current working directory to the project root directory
os.chdir(project_root)

load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Mat2DevPlatform.settings")

from django.conf import settings
import openai
import numpy as np



openai.api_key = settings.OPENAI_API_KEY

print(openai.api_key)






def get_text_embeddings(texts):
    """
    Retrieve text embeddings for a list of texts using OpenAI's text-embedding-ada-002.

    :param texts: List of text strings.
    :return: List of text embeddings.
    """
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=texts
    )

    return response["data"]


# Loading from web
# battinfo = get_ontology('../Ontology/BattINFO/battinfo.ttl').load()
# # Print the classes in the ontology
# print("Start")
# for cls in battinfo.classes():
#     print(cls)
# print("Done")

def find_most_similar_description(main_description, candidate_descriptions):
    """
    Compare an ontology class description with a list of candidate descriptions and find the most similar one.

    :param main_description: The main ontology class description (str).
    :param candidate_descriptions: A list of candidate descriptions (List[str]).
    :return: The index of the most similar description and its similarity score.
    """
    # Get text embeddings for the main description and candidate descriptions
    all_descriptions = [main_description] + candidate_descriptions
    print("hier?")
    for i, description in enumerate(all_descriptions):
        all_descriptions[i] = preprocess(description)
        print(all_descriptions[i])
    embeddings = get_text_embeddings(all_descriptions)

    main_embedding = np.array(embeddings[0]["embedding"])
    candidate_embeddings = np.array([embedding["embedding"] for embedding in embeddings[1:]])

    # Calculate cosine similarity between the main description and candidate descriptions
    dot_product = np.dot(candidate_embeddings, main_embedding)
    norms = np.linalg.norm(candidate_embeddings, axis=1) * np.linalg.norm(main_embedding)
    cosine_similarities = dot_product / norms

    # Find the index of the most similar description and its similarity score
    most_similar_index = np.argmax(cosine_similarities)
    most_similar_score = cosine_similarities[most_similar_index]

    return most_similar_index, most_similar_score, cosine_similarities

# Example usage


def main():
    # main_description = "Li Battery."
    # # noinspection PyPackageRequirements
    # candidate_descriptions = [
    #     "battery containing a non-aqueous electrolyte and a negative electrode of lithium or containing lithium.",
    #     "metal air electrochemical cell with an alkaline electrolyte and a negative electrode of zinc.",
    #     "battery which supplies electric energy to an electric circuit when the normal power supply of this electric circuit is interrupted.",
    #     "An electrochemical cell which is not designed to be electrically recharged.",
    #     "cell having, at a specified temperature, an invariant and specific open-circuit voltage, used as a reference voltage.",
    #     "basic functional unit, consisting of an assembly of electrodes, electrolyte, container, terminals and usually separators, that is a source of electric energy obtained by direct conversion of chemical energy.",
    #     "One or more cells fitted with devices necessary for use, for example case, terminals, marking and protective devices.",
    #     "Atom subclass for lithium.",
    #     "Insertion electrode made out of Lithium"
    # ]
    #
    # most_similar_index, most_similar_score, vector = find_most_similar_description(main_description, candidate_descriptions)
    # print(f"The most similar description for the following description: \n {main_description} \n Matching Description: \n         {candidate_descriptions[most_similar_index]} \n Similarity score: {most_similar_score}")
    # print("The other Descritptions with the similarity score:")
    # for sim, des in zip(vector, candidate_descriptions):
    #     print("\t",sim,des)


    # Load the ontology from a local file or a URL
    ontology_file = "manufactured.owl"
    onto = get_ontology(ontology_file).load()

    # Get the classes in the ontology
    classes = list(onto.classes())
    class onto_name(AnnotationProperty):
        namespace = onto
    # Print the classes
    for cls in classes:
        if not cls.onto_name:
            print(cls)
            add_description_to_class(cls.name, onto)

if __name__ == "__main__":
    main()