LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Mat2DevPlatform/Mat2DevAPI/data/Lukas/fabrication/fabrication.csv' AS row

MATCH(emmo_ink:EMMO_Matter {EMMO__name: "CatalystInk"})
MATCH(emmo_ic:EMMO_Quantity {EMMO__name: "CatalystIonomerRatio"})
MERGE(ink:Material:Matter {name: row.name, date_added: "heute"})
ON CREATE
SET ink.uid = randomUUID()
MERGE(ink)-[:IS_A]->(emmo_ink)

MERGE(ic:Property {name: row.name+"_ic"})
MERGE(ink)-[:HAS_PROPERTY{value: row.IC}]->(ic)
MERGE(ic)-[:IS_A]->(emmo_ic)
