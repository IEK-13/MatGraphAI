from update.update_db import upload_query, install_models
from neo4jqueries.cypherqueries import import_data_query
from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
                      FloatProperty, UniqueIdProperty, RelationshipTo)

config.DATABASE_URL = 'bolt://neo4j:herrklo1@localhost:11003/test'  # default

install_models()

print("Finished importing models")

#upload_query(import_data_query)
