# Generated by Django 3.2.13 on 2022-08-09 07:31

from django.db import migrations
from neomodel import db


def remove_current_situation(apps, schema_editor):
    results, meta = db.cypher_query(
        'MATCH (p:WorkProfile) WHERE p.current_situation IS NOT NULL REMOVE p.current_situation'
    )

class Migration(migrations.Migration):

    dependencies = [
        ('skills', '0008_auto_20220801_1405'),
    ]

    operations = [
        migrations.RunPython(remove_current_situation)
    ]
