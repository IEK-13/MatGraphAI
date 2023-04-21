import json
import os

import pandas as pd
from neomodel import db
from fuzzywuzzy import process
from Mat2DevAPI.models.metadata import *  # Import your models here
from django.shortcuts import render
from Mat2DevAPI.importer.import_pubchem_json import IMPORT_PUBCHEM
from pprint import pprint

def map_measurement_data(csv_data):
    # Implement your mapping logic for measurement data here
    return csv_data

def map_materials_data(csv_data):
    # Implement your mapping logic for materials data here
    return csv_data

def map_simulation_data(csv_data):
    # Implement your mapping logic for simulation data here
    return csv_data

def map_fabrication_data(csv_data):
    # Implement your mapping logic for fabrication data here
    return csv_data

def map_metadata(csv_data):
    # Implement your mapping logic for fabrication data here
    return csv_data



def find_best_match(name, choices):
    best_match, score = process.extractOne(name, choices)
    if score > 80:  # Adjust the threshold based on your requirements
        return best_match
    else:
        raise ValueError(f"No match found for '{name}'")

# Import your models here









DATA_TYPE_MAPPING = {
    'measurement': map_measurement_data,
    'materials': map_materials_data,
    'simulation': map_simulation_data,
    'fabrication': map_fabrication_data,
    'metadata': map_metadata
}

def map_csv_data_to_graph(csv_data, data_type, header):
    """Analyze and map the CSV data to the graph database schema.

    Args:
        csv_data: A list of dictionaries representing the data from the CSV file.
        data_type: A string representing the selected data type.

    Returns:
        A list of dictionaries with the mapped data.
    """
    if data_type in DATA_TYPE_MAPPING:
        mapping_function = DATA_TYPE_MAPPING[data_type]
        mapped_data = mapping_function(csv_data, header)
        return str(mapped_data)
    else:
        raise ValueError(f"Unsupported data type: {data_type}")



def upload_csv(request):

    if request.method == 'POST':
        # Get the uploaded CSV file and the selected data type
        csv_file = request.FILES['file']
        data_type = request.POST['data_type']

        # Parse the CSV data into a Pandas DataFrame
        data = pd.read_csv(csv_file)

        # Analyze and map the CSV data to the graph database schema
        mapped_data = map_csv_data_to_graph(data, data_type, data.columns)

        # Insert the mapped data into Neo4j using the appropriate Cypher query
        cypher_query = IMPORT_PUBCHEM.replace('$data', mapped_data)
        # print(cypher_query)
        db.cypher_query(cypher_query)

        # Save the uploaded CSV file to the server's media directory
        csv_file_name = csv_file.name
        csv_file_path = os.path.join('/home/mdreger/Documents/data/backup', csv_file_name)
        with open(csv_file_path, 'wb+') as destination:
            for chunk in csv_file.chunks():
                destination.write(chunk)

        # Pass the results to the results view function
        return render(request, 'results.html', {'data': json_data})
    else:
        # Render the upload form
        return render(request, 'upload.html')



