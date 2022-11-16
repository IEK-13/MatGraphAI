LOAD CSV WITH HEADERS FROM 'file:///elements.csv' AS line

// Create Nodes
CREATE (element:Element {name: line.name, summary: line.summary, abbreviation : line.symbol})


FOREACH(x IN CASE WHEN line.discovered_by IS NOT NULL THEN [1] END |
MERGE (researcher:Researcher {uid: randomUUID(), name: line.discovered_by})
CREATE (exp:Manufacturing {uid: randomUUID()})
MERGE (element)<-[:YIELDED]-(exp)-[:BY]->(researcher)
// IntegerProperties
CREATE (element)-[HAS_INTEGER_PROPERTY {value : toInteger(line.number}]->(:EMMO_Quantity {EMMO_name: "AtomicNumber"})

//FloatProperties
CREATE (element)-[HAS_FLOAT_PROPERTY {value : toFloat(line.number}]->(:EMMO_Quantity {EMMO_name: "AtomicMass"})
CREATE (element)-[HAS_FLOAT_PROPERTY {value : toFloat(line.atomic_mass}]->(:EMMO_Quantity {EMMO_name: "AtomicMass"})
CREATE (element)-[HAS_FLOAT_PROPERTY {value : FloatProperty(line.number}]->(:EMMO_Quantity {EMMO_name: "MolarHeat"})
CREATE (element)-[HAS_FLOAT_PROPERTY {value : FloatProperty(line.density}]->(:EMMO_Quantity {EMMO_name: "Density"})

// 