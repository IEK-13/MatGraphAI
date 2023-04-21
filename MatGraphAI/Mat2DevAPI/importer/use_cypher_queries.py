from Mat2DevPlatform.Mat2DevAPI.useful_queries import *
from neomodel import db


def upload_query(query):
    db.cypher_query(query)


if __name__ == "__main__":
    print("upload queries")
    upload_query()