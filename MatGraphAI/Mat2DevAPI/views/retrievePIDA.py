from django.shortcuts import render
from Mat2DevAPI.models.metadata import PIDA

from django.http import JsonResponse, HttpResponse
import csv
import json
from neomodel import config, db


def download_data_form(request, PID):
    return render(request, 'PIDA.html', {'PID': PID})
def download_data(request, PID):
    # Connect to Neo4j database

    # Query to fetch data by PID
    query = '''
    MATCH (n:PIDA {PIDA: $PID})-[:CONTAINS]->(connected_nodes)
    WITH connected_nodes, labels(connected_nodes) as node_labels, properties(connected_nodes) as node_properties
    UNWIND node_labels as label
    RETURN label, node_properties
    ORDER BY label
    '''

    # Execute query and fetch data
    results = db.cypher_query(query, {'PID':PID})
    print(results)

    # Choose output format: 'csv' or 'json'
    output_format = request.GET.get('format', 'csv').lower()

    if output_format == 'csv':
        # Prepare CSV file
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="data_{PID}.csv"'

        # Get field names (column names)
        fieldnames = results[0][0][1].keys()

        writer = csv.DictWriter(response, fieldnames=fieldnames)
        writer.writeheader()

        for row in results[0]:
            writer.writerow(row[1])

        return response
    elif output_format == 'json':
        # Prepare JSON file
        response = JsonResponse([{row[0]: row[1]} for row in results[0]], safe=False)
        response['Content-Disposition'] = f'attachment; filename="data_{PID}.json"'
        return response
    else:
        # Return an error response for invalid formats
        return HttpResponse("Invalid format. Supported formats: 'csv' and 'json'.", status=400)
