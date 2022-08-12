from neomodel import (db, config)
#from ProjectLib.neo4jqueries.cypherqueries import *
from neo4j import exceptions
from os import system


#def install_models():
# install_models    try:
#         system(
#             """neomodel_install_labels ProjectLib.models ProjectLib/models/*.py --db bolt://neo4j:herrklo1@localhost:11005/test2""")
#     except:
#         print("class already included")
#         pass
#
#
# def upload_query(query):
#     config.DATABASE_URL = 'bolt://neo4j:herrklo1@localhost:11005/test2'
#     for el in query:
#         print(el)
#         db.cypher_query(el)
