import csv

from skills.models.education import Subject
from skills import OntologyOccupation
from neomodel import db


QUERY = '''
    MATCH
        (occ:OntologyOccupation)<-[:RELEVANT_FOR]-(skill:Skill)
    WHERE
        occ.uid in $occupations
    WITH
        DISTINCT skill,
        count(skill) as relevance
    ORDER BY relevance DESC
    LIMIT 100
    MATCH
        (course:Course)-[:IS]->(subject:Subject)
    WHERE
        subject.uid=$subject
    CREATE
        (course)-[:TEACHES {priority: relevance}]->(skill)
'''


with db.transaction:
    with open('courses.csv') as csvfile:

        reader = csv.DictReader(csvfile, delimiter=';')

        for row in reader:

            subject = row['Studienrichtung']

            try:
                subject = Subject.nodes.get(label=subject)

                occupations = []

                for col, value in row.items():
                    if col.startswith("Full Job"):
                        if value:
                            try:
                                occupations.append(
                                    OntologyOccupation.nodes.get(label=value).uid
                                )
                            except OntologyOccupation.DoesNotExist:
                                print(f'occupation not found: {value}')

                results, meta = db.cypher_query(
                    QUERY, {
                        'occupations': occupations,
                        'subject': subject.uid
                    }
                )

            except Subject.DoesNotExist:
                print(f"subject not found: {subject}")


