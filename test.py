from py2neo import Graph
graph = Graph('http:/172.18.0.52:7474', user='neo4j',password='123')
tx = graph.begin()
for name in ["Alice", "Bob", "Carol"]:
    tx.append("CREATE (person:Person name: $name) RETURN person", name=name)
alice, bob, carol = [result.one for result in tx.commit()]
