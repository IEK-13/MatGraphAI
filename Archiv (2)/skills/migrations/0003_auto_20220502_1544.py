# Generated by Django 3.1.13 on 2022-05-02 13:44

from django.db import migrations
from neomodel import db


def add_current_situation(apps, schema_editor):
    results, meta = db.cypher_query(
        'MATCH (p:WorkProfile) WHERE NOT EXISTS(p.current_situation) SET p.current_situation="in_education"'
    )


class Migration(migrations.Migration):

    dependencies = [
        ('skills', '0002_auto_20220404_1508'),
    ]

    operations = [
        migrations.RunPython(add_current_situation)
    ]
