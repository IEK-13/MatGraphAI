PROFILE
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Mat2DevPlatform/Mat2DevAPI/data/lukas/fabrication/fabrication.csv' AS row
MATCH(met:Element {name:row.catalyst2})
MATCH(emmo_ink:EMMO_Matter {EMMO__name: "CatalystInk"})
MATCH(emmo_ionomer:EMMO_Matter {EMMO__name: "Nafion_D2021CS"})
MATCH(emmo_ic:EMMO_Quantity {EMMO__name: "CatalystIonomerRatio"})
MATCH(emmo_cc:EMMO_Quantity {EMMO__name: "CatalystCarbonRatio"})
MATCH(emmo_h20:EMMO_Matter {EMMO__name: "Water"})
MATCH(emmo_propanol:EMMO_Matter {EMMO__name: "1-Propanol"})
MATCH(emmo_cs:EMMO_Matter {EMMO__name: row.catalyst1})
MATCH(emmo_met:EMMO_Matter {EMMO__name: row.catalyst2})
MATCH(emmo_cat:EMMO_Matter {EMMO__name: row.cat_emmo})
MATCH(researcher:Researcher {first_name: "Lukas"})
MERGE(ink:Material {name: row.name,
                           date_added: date(),
                           flag: "findich"
})
ON CREATE
SET ink.uid = randomUUID()

MERGE(inkfab:Manufacturing {run_title: row.name+ "_mixing",
                            date_added : date(),
                            flag: "findich"
})
  ON CREATE
  SET inkfab.uid = randomUUID()
MERGE(inkfab)-[:IS_MANUFACTURING_OUTPUT]->(ink)

MERGE(ink)-[:IS_A]->(emmo_ink)
MERGE(ic:Property {name: row.name+"_ic"})
MERGE(ink)-[:HAS_PROPERTY{value: row.IC}]->(ic)
MERGE(ic)-[:IS_A]->(emmo_ic)
FOREACH(ignoreMe IN CASE WHEN row.ionomer is not null THEN [1] ELSE [] END|

  MERGE(ionomer:Material {name: row.ionomer, date_added: date()})
  MERGE(ink)-[:HAS_PART]->(ionomer)
  MERGE(ionomer)-[:IS_A]->(emmo_ionomer)
  MERGE(ionomer)-[:IS_MANUFACTURING_INPUT]->(inkfab)
)
MERGE(sol1:Material {name: row.solvent1, date_added: date()})
MERGE(sol2:Material {name: row.solvent2, date_added: date()})
MERGE(solfab:Manufacturing {run_title: row.solvent1+"_"+row.solvent2+"_"+row.solvent1_ratio+ "_fabrication",
                            date_added : date(),
                            flag: "findich"
})
  ON CREATE
  SET solfab.uid = randomUUID()
MERGE(sol:Molecule {name: row.solvent1+"_"+row.solvent2+"_"+row.solvent1_ratio, date_added: date()})
MERGE(solfab)-[:IS_MANUFACTURING_OUTPUT]->(sol)
MERGE(sol1)-[:IS_MANUFACTURING_INPUT]->(solfab)
MERGE(sol2)-[:IS_MANUFACTURING_INPUT]->(solfab)
MERGE(sol)-[:IS_MANUFACTURING_INPUT]->(inkfab)

MERGE(sol1)<-[:HAS_PART {value: TOFLOAT(row.solvent1_ratio)}]-(sol)
MERGE(sol2)<-[:HAS_PART {value: TOFLOAT(1-TOFLOAT(row.solvent1_ratio))}]-(sol)
MERGE(sol1)-[:IS_A]->(emmo_propanol)
MERGE(sol2)-[:IS_A]->(emmo_h20)


MERGE(ink)-[:HAS_PART]->(sol)


MERGE(catfab:Manufacturing {run_title: row.catalyst2 + "_" + row.wt+ "_fabrication",
                            date_added : date(),
                            flag: "findich"
})
  ON CREATE
  SET solfab.uid = randomUUID()

MERGE(cs:Material {name:row.catalyst1, date_added: date()})
MERGE(cat:Material {name:row.catalyst2 + "_" + row.wt, date_added: date()})
MERGE(sol)-[:IS_MANUFACTURING_INPUT]->(inkfab)
MERGE(cat)-[:IS_MANUFACTURING_INPUT]->(inkfab)
MERGE(cat)-[:IS_A]->(emmo_cat)
MERGE(catfab)-[:IS_MANUFACTURING_OUTPUT]->(cat)

WITH row, cat,cs ,ink, met, emmo_met, emmo_cs, inkfab, solfab, researcher
OPTIONAL MATCH(emmo_ox:EMMO_Matter {EMMO__name: row.catalyst3})
FOREACH(ignoreMe IN CASE WHEN row.catalyst3 is not null THEN [1] ELSE [] END|
  MERGE(ox:Element {name:row.catalyst3})
  MERGE(ox)-[:IS_A]->(emmo_ox)
  MERGE(ox)<-[:HAS_PART]-(cat)
  MERGE(sol)-[:IS_MANUFACTURING_INPUT]->(catfab)
)
WITH row, cat,cs ,ink, met, emmo_met, emmo_cs,inkfab,solfab, researcher

MERGE(met)-[:IS_A]->(emmo_met)
MERGE(cs)-[:IS_A]->(emmo_cs)



MERGE(cs)<-[:HAS_PART]-(cat)
MERGE(met)<-[:HAS_PART]-(cat)

MERGE(cat)-[:HAS_PART]->(ink)

MERGE(inkmain:Manufacturing {run_title: row.name+ "_fabrication",
                            date_added : date(),
                            flag: "findich"
})
  ON CREATE
  SET inkmain.uid = randomUUID()

MERGE(inkmain)-[:HAS_PART]->(inkfab)
MERGE(inkmain)-[:HAS_PART]->(solfab)
MERGE(inkmain)-[:HAS_PART]->(catfab)

MERGE(inkfab)-[:BY]->(researcher)
MERGE(inkmain)-[:BY]->(researcher)
MERGE(catfab)-[:BY]->(researcher)
MERGE(solfab)-[:BY]->(researcher)