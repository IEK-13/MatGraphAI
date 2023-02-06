PROFILE
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Mat2DevPlatform/Mat2DevAPI/data/Lukas/fabrication/fabrication.csv' AS row

MATCH(emmo_ink:EMMO_Matter {EMMO__name: "CatalystInk"})
MATCH(emmo_ic:EMMO_Quantity {EMMO__name: "CatalystIonomerRatio"})
MATCH(emmo_ic:EMMO_Quantity {EMMO__name: "CatalystIonomerRatio"})
MATCH(emmo_cc:EMMO_Quantity {EMMO__name: "CatalystCarbonRatio"})
MERGE(ink:Material:Matter {name: row.name, date_added: "heute"})
ON CREATE
SET ink.uid = randomUUID()
MERGE(ink)-[:IS_A]->(emmo_ink)

MERGE(ic:Property {name: row.name+"_ic"})
MERGE(ink)-[:HAS_PROPERTY{value: row.IC}]->(ic)
MERGE(ic)-[:IS_A]->(emmo_ic)
FOREACH(ignoreMe IN CASE WHEN row.ionomer is not null THEN [1] ELSE [] END|

  MERGE(ionomer:Matter:Material {EMMO__name: row.ionomer, date_added: "heute"})

)
MERGE(sol1:Matter:Material {EMMO__name: row.solvent1, date_added: "heute"})
MERGE(sol2:Matter:Material {EMMO__name: row.solvent2, date_added: "heute"})
MERGE(sol:Matter:Material {EMMO__name: row.solvent1+"_"+row.solvent2+"_"+row.solvent1_ratio, date_added: "heute"})
MERGE(sol1)<-[:HAS_PART {value: TOFLOAT(row.solvent1_ratio)}]-(sol)
MERGE(sol2)<-[:HAS_PART {value: TOFLOAT(1-TOFLOAT(row.solvent1_ratio))}]-(sol)

MERGE(ink)-[:HAS_PART]->(sol)


MERGE(cat:Matter:Material {name:row.catalyst2 + "_" + row.wt, date_added: "heute"})
MERGE(cs:Matter:Material {name:row.catalyst1, date_added: "heute"})
MERGE(met:Matter:Material {name:row.catalyst2, date_added: "heute"})
FOREACH(ignoreMe IN CASE WHEN row.catalyst3 is not null THEN [1] ELSE [] END|

  MERGE(ox:Matter:Material {name:row.catalyst3, date_added: "heute"})

)
MERGE(cs)<-[:HAS_PART]-(cat)
MERGE(met)<-[:HAS_PART]-(cat)
MERGE(ox)<-[:HAS_PART]-(cat)


