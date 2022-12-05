// Molecule import starts here

LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Mat2DevPlatform/Mat2DevAPI/data/PubChemMolecules_sum.csv' AS row

MATCH (mw:EMMO_Quantity {EMMO__name: "MolecularWeight"}),
      (c:Element {symbol: "C"}),
      (h:Element {symbol: "H"}),
      (o:Element {symbol: "O"}),
      (n:Element {symbol: "N"}),
      (f:Element {symbol: "F"}),
      (s:Element {symbol: "S"})




MERGE(solvent:Molecule {name: row.cmpdname,
                         SMILES : row.isosmiles,
                         InChi_Key : row.inchikey,
                         IUPAC_name : row.iupacname,
                         InChi: row.inchi,
                         chemical_formula: row.mf})


FOREACH(x IN CASE WHEN row.C IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.C)}]->(c))

FOREACH(x IN CASE WHEN row.H IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.H)}]->(h))

FOREACH(x IN CASE WHEN row.O IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.O)}]->(o))

FOREACH(x IN CASE WHEN row.N IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.N)}]->(n))

FOREACH(x IN CASE WHEN row.F IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.F)}]->(f))

FOREACH(x IN CASE WHEN row.S IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.S)}]->(s))

FOREACH(x IN CASE WHEN row.ontologylabel2 IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:IS_A ]->(EMMO_Material {EMMO__name: row.ontologylabel2}))

FOREACH(x IN CASE WHEN row.ontologylabel1 IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:IS_A ]->(EMMO_Material {EMMO__name: row.ontologylabel1}))

FOREACH(x IN CASE WHEN toFloat(row.mw) IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_FLOAT_PROPERTY {value: toFloat(row.mw)}]->(mw));


