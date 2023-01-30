MERGE (vb:Matter:Material {
name: "VULCAN XC72",
date_added: "1111-11-11"
})
ON CREATE
SET vb.uid = randomUUID()
MERGE (cb:Matter:Material {
  name: "Carbon Black",
  date_added: "1111-11-11"
})
ON CREATE
SET cb.uid = randomUUID()

WITH cb, vb
MATCH(c:Matter:Material {symbol: "C"})
MATCH(emmo_cb:EMMO_Matter {EMMO__name: "CarbonBlack"})
MERGE(vb)-[:IS_A]->(emmo_cb)
MERGE(cb)-[:IS_A]->(emmo_cb)
MERGE(vb)-[:HAS_PART]->(c)
MERGE(cb)-[:HAS_PART]->(c);


LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Mat2DevPlatform/Mat2DevAPI/data/Catalysts.csv' AS row
MATCH (ontology:EMMO_Matter {EMMO__name:row.Ontology})
MERGE(cat:Matter:Material{name: row.Name,
                   chemical_formula: row.ChemicalFormula,
                   date_added: "1111-11-11"
})
  ON CREATE
  SET cat.uid = randomUUID()
MERGE(cat)-[:IS_A]->(ontology)
SET cat.name = row.Name,  cat.CAS = row.CAS


WITH row, cat
MATCH(cat:Matter:Material{name: row.Name, chemical_formula: row.ChemicalFormula})
MATCH (part1:Matter {symbol:row.HasPart1})
MERGE(cat)-[:HAS_PART]->(part1)

WITH row, cat
MATCH(cat:Matter:Material{name: row.Name, chemical_formula: row.ChemicalFormula})
MATCH (part2:Matter {name:row.HasPart2})
MERGE(cat)-[:HAS_PART]->(part2)


WITH row, cat
MATCH(cat:Matter:Material{name: row.Name, chemical_formula: row.ChemicalFormula})
MATCH (part3:Matter {symbol:row.HasPart3})
MERGE(cat)-[:HAS_PART]->(part3)

WITH row, cat
MATCH (part3:Matter {symbol:row.HasPart3})
MERGE(test)-[:HAS_PART]->(part3);

LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Mat2DevPlatform/Mat2DevAPI/data/Catalysts.csv' AS row
MATCH(cat:Material{name: row.Name, chemical_formula: row.ChemicalFormula})
MATCH(emmo_purity:EMMO_Quantity{EMMO__name: "MetalPurity"})
FOREACH(x IN CASE WHEN row.Purity IS NOT NULL THEN [1] END |
MERGE (purity:Property {name:row.Name+ "_purity"})
MERGE(purity)-[:IS_A]->(emmo_purity)
ON CREATE
SET purity.uid = randomUUID()
MERGE(cat)-[:HAS_PROPERTY {value: row.Purity}]->(purity)
)

WITH row, cat
MATCH (emmo_ratio:EMMO_Quantity {EMMO__name:row.CatalystIonnomerRatio})
MERGE (ratio:Property {name:row.Name+ "_ratio"})
MERGE(ratio)-[:IS_A]->(emmo_ratio)
MERGE(cat)-[:HAS_PROPERTY {value: row.CatalystIonnomerRatio}]->(ratio)
C