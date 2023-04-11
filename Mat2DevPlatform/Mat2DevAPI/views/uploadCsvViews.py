import csv
import json
import os
from neomodel import db

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from Mat2DevAPI.importer.import_pubchem_json import IMPORT_PUBCHEM, IMPORT_RESEARCHER


def results(request, url, json_data):
    """Render the results template with the extracted data.

    Args:
        request: The HTTP request object.
        url: The URL of the uploaded CSV file.
        json_data: A list of dictionaries representing the data from the CSV file.

    Returns:
        A rendered HTML template containing the CSV file upload results.
    """
    return render(request, 'results.html', {'data': json_data})


def upload_csv(request):
    """Handle file uploads and convert CSV to JSON.

    If the request method is POST, extract the data from the uploaded CSV file,
    convert it to a JSON object, save the CSV file locally, and use the Cypher query
    to insert the data into Neo4j. If the request method is GET, render the upload form.

    Args:
        request: The HTTP request object.

    Returns:
        If the request method is POST, a call to the results view function. If the
        request method is GET, a rendered HTML template containing an upload form.
    """
    if request.method == 'POST':
        # Get the uploaded CSV file
        csv_file = request.FILES['file']

        # Parse the CSV data into a list of dictionaries
        csv_data = csv.reader(csv_file.read().decode('utf-8').splitlines())
        json_data = []
        header = None
        for row in csv_data:
            if not header:
                # If this is the first row, set the header list
                header = row
            else:
                # Otherwise, create a dictionary mapping headers to data
                data = {}
                for i in range(len(header)):
                    data[header[i]] = row[i]
                json_data.append(data)
                # Insert the data into Neo4j using the given Cypher query
        input_data = json.dumps(json_data).replace("'", "")
        cypher_query = IMPORT_PUBCHEM.replace('$data', input_data)
        print(cypher_query)
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

