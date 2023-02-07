PROFILE
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Mat2DevPlatform/Mat2DevAPI/data/Lukas/fabrication/fabrication.csv' AS row

MATCH(emmo_ink:EMMO_Matter {EMMO__name: "CatalystInk"})
MATCH(emmo_ionomer:EMMO_Matter {EMMO__name: "Nafion_D2021CS"})
MATCH(emmo_ic:EMMO_Quantity {EMMO__name: "CatalystIonomerRatio"})
MATCH(emmo_cc:EMMO_Quantity {EMMO__name: "CatalystCarbonRatio"})
MATCH(emmo_h20:EMMO_Matter {EMMO__name: "Water"})
MATCH(emmo_propanol:EMMO_Matter {EMMO__name: "1-Propanol"})
MATCH(emmo_cs:EMMO_Matter {EMMO__name: row.catalyst1})
MATCH(emmo_met:EMMO_Matter {EMMO__name: row.catalyst2})
MATCH(emmo_cat:EMMO_Matter {EMMO__name: row.emmo_cat})
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
MERGE(sol1)-[:IS_A]->(emmo_propanol)
MERGE(sol2)-[:IS_A]->(emmo_h20)
MERGE(ionomer)-[:IS_A]->(emmo_ionomer)


MERGE(ink)-[:HAS_PART]->(sol)
MERGE(ink)-[:HAS_PART]->(ionomer)




MERGE(cs:Matter:Material {name:row.catalyst1, date_added: "heute"})
MERGE(cat:Matter:Material {name:row.catalyst2 + "_" + row.wt, date_added: "heute"})

MERGE(met:Matter:Element {name:row.catalyst2 , date_added: "heute"})
WITH row, cat,cs ,ink, met, emmo_met, emmo_cs
OPTIONAL MATCH(emmo_ox:EMMO_Matter {EMMO__name: row.catalyst3})
FOREACH(ignoreMe IN CASE WHEN row.catalyst3 is not null THEN [1] ELSE [] END|
  MERGE(ox:Matter:Element {name:row.catalyst3, date_added: "heute"})
  MERGE(ox)-[:IS_A]->(emmo_ox)
  MERGE(ox)<-[:HAS_PART]-(cat)
)
WITH row, cat,cs ,ink, met, emmo_met, emmo_cs

MERGE(met)-[:IS_A]->(emmo_met)
MERGE(cs)-[:IS_A]->(emmo_cs)



MERGE(cs)<-[:HAS_PART]-(cat)
MERGE(met)<-[:HAS_PART]-(cat)

MERGE(cat)-[:HAS_PART]->(ink)

