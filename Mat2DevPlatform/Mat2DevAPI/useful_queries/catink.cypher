LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Mat2DevPlatform/Mat2DevAPI/data/CatInkFabrication.csv' AS row

MATCH (ink:Material {name: row.`Run #`})-[:IS_A]-(:EMMO_Material {EMMO__name: "CatalystInk"}),
      (EMMO_cathode:EMMO_Manufactured{EMMO__name: "Cathode"}),
      (EMMO_thickness:EMMO_Quantity{EMMO__name: "Thickness"}),
      (EMMO_porosity:EMMO_Quantity{EMMO__name: "Porosity"}),
      (EMMO_cclfab:EMMO_Manufacturing {EMMO__name: "CCLManufacturing"})

// Process Nodes
MERGE(cclfab:Manufacturing {run_title: row.`Run #`,
                            uid: randomUUID(),
                           DOI: row.DOI,
                           date_added : "1111-11-11"
})


//Material Nodes
MERGE(ccl:Material {name: row.`Run #`,
                                 date_added: "1111-11-11"})
  ON CREATE
  SET ccl.uid = randomUUID()

// Measurement nodes
MERGE(sem:Measurement{uid: randomUUID(),
                     DOI: row.DOI,
                     date_added : "1111-11-11"
})
MERGE(thickness:Property{uid: randomUUID(),
                      date_added : "1111-11-11"
})
MERGE(thickness:Property{uid: randomUUID(),
                         date_added : "1111-11-11"
})
MERGE(ccl)-[:IS_MEASUREMENT_INPUT]->(sem)-[:YIELDS_FLOAT_PROPERTY{
  value: TOFLOAT(row.`SEM thickness STD (µm)`)}]->(thickness)-[:IS_A]->(EMMO_thickness)
MERGE(ccl)-[:IS_MEASUREMENT_INPUT]->(sem)-[:YIELDS_FLOAT_PROPERTY{
  value: TOFLOAT(row.`SEM thickness STD (µm)`)}]->(porosity)-[:IS_A]->(EMMO_thickness)
MERGE(porosity)-[:DERIVED_FROM]->(thickness)

//Labeling
MERGE(ccl)-[:IS_A]->(EMMO_cathode)
MERGE(cclfab)-[:IS_A]->(EMMO_cclfab)

// Processing
MERGE(ink)-[:IS_MANUFACTURING_INPUT]->(cclfab)
MERGE(cclfab)-[:IS_MANUFACTURING_OUTPUT]->(ccl)