from neomodel import db
from neo4jqueries.cypherqueries import (import_data_query)
import os


def install_models():
    os.system(
        """neomodel_install_labels db.models db/models/*.py --db bolt://neo4j:herrklo1@localhost:11003/test""")


def upload_query(query):
    db.cypher_query(query)
