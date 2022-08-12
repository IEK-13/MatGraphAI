from neomodel import DateTimeProperty, config


def test():
    config.DATABASE_URL = 'bolt://neo4j:herrklo1@localhost:11005/test2'
    print("k")
