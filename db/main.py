from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
                      FloatProperty, UniqueIdProperty, RelationshipTo)
from update.update_db import upload_query, install_models
from neo4jqueries.cypherqueries import (import_data_query, import_elements_query,
                                        import_fabians_data_query)


config.DATABASE_URL = 'bolt://neo4j:herrklo1@localhost:11005/test1'  # default

install_models()

print("Finished importing models")
upload_query(import_fabians_data_query)
upload_query(import_elements_query)
upload_query(import_data_query)
