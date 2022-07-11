from neomodel import (db, config)
from neo4jqueries.cypherqueries import *
from neo4j import exceptions
from os import system
import models


def install_models():
    try:
        system(
            """neomodel_install_labels db.models db/models/*.py --db bolt://neo4j:herrklo1@localhost:11005/test""")
    except:
        print("class already included")
        pass


def upload_query(query):
    config.DATABASE_URL = 'bolt://neo4j:herrklo1@localhost:11005/test'
    for el in query:
        print(el)
        db.cypher_query(el)
