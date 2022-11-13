# Generated by Django 3.2.13 on 2022-07-28 09:17

from django.db import migrations
from neomodel import db


# migrates old IS/STUDIES rels to new CV format
def migrate_cv(apps, schema_editor):

    with db.write_transaction:

        db.cypher_query(
            '''
            MATCH
                (wp:WorkProfile)-[old_rel:IS]->(occ:OntologyOccupation)
            CREATE
                (wp)-[:WORKED_AS {title: occ.label}]->(occ)
            DELETE old_rel
            '''
        )

        db.cypher_query(
            '''
            MATCH
                (wp:WorkProfile)-[old_rel:STUDIES]->(course:Course),
                (course)-[:IS]->(subject:Subject),
                (course)-[:IS]->(degree:Degree)
            CREATE
                (wp)-[:STUDIED {title: subject.label, school: old_rel.school, degree: degree.uid}]->(subject)
            DELETE old_rel
            '''
        )


class Migration(migrations.Migration):

    dependencies = [
        ('skills', '0006_auto_20220701_2327'),
    ]

    operations = [
        migrations.RunPython(migrate_cv)
    ]
