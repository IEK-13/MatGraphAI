LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Mat2DevPlatform/Mat2DevAPI/data/CatInkFabrication.csv' AS row

MATCH (ink:Material {name: row.`Run #`})-[:IS_A]-(:EMMO_Material {EMMO__name: "CatalystInk"}),
      (EMMO_cathode:EMMO_Manufactured{EMMO__name: "Cathode"})

// Process Nodes
MERGE(cclfab:Manufacturing {run_title: row.`Run #`,
                           DOI: row.DOI,
                           date_added : "1111-11-11"
})
  ON CREATE
  SET coatingsubstrate.uid = randomUUID()

//Material Nodes
MERGE(ccl:Material {name: row.`Run #`,
                                 date_added: "1111-11-11"})
  ON CREATE
  SET coatingsubstrate.uid = randomUUID()

// Measurement nodes

//Labeling
MERGE(ccl)-[:IS_A]->(EMMO_cathode)

// Processing
MERGE(ink)-[:IS_MANUFACTURING_INPUT]->(cclfab)
MERGE(cclfab)-[:IS_MANUFACTURING_OUTPUT]->(ccl)