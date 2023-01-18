MERGE (vb:Material {
name: "VULCAN XC72"
})
MERGE (cb:Material {
  name: "Carbon Black"
})
WITH cb, vb
MATCH(emmo_cb:EMMO_Matter {EMMO__name: "CarbonBlack"})
MERGE(vb)-[:IS_A]->(emmo_cb)
MERGE(cb)-[:IS_A]->(emmo_cb);


LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Mat2DevPlatform/Mat2DevAPI/data/Catalysts.csv' AS row
MERGE(cat:Material{chemical_formula: row.ChemicalFormula})
SET cat.name = row.Name,  cat.CAS = row.CAS

WITH cat, row
MATCH (part1:Element {symbol:row.HasPart1})
MERGE(cat)-[:HAS_PART]->(part1)

WITH cat, row
MATCH (part2:Material {name:row.HasPart2})
MERGE(cat)-[:HAS_PART]->(part2)

WITH cat, row
MATCH (part3:Element {symbol:row.HasPart3})
MERGE(cat)-[:HAS_PART]->(part3)

WITH cat, row
MATCH (ontology:EMMO_Matter {EMMO__name:row.Ontology})
MERGE(cat)-[:IS_A]->(ontology)
