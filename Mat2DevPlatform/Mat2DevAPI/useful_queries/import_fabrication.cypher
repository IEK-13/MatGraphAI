LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Mat2DevPlatform/Mat2DevAPI/data/FuelCellFabrication.csv' AS row

MATCH (EMMO_fcas:EMMO_Manufacturing {EMMO__name: "FuelCellAssembly"}),
      (EMMO_meaas:EMMO_Manufacturing {EMMO__name: "CCMManufacturing"}),
      (EMMO_membrane:EMMO_Manufactured{EMMO__name: "Membrane"}),
      (EMMO_mea:EMMO_Manufactured{EMMO__name: "CCM"}),
      (EMMO_fc:EMMO_Manufactured{EMMO__name: "FuelCell"}),
      (EMMO_bp:EMMO_Manufactured{EMMO__name: "BipolarPlate"}),
      (EMMO_gdl:EMMO_Manufactured{EMMO__name: "GasDiffusionLayer"})




// MEA and FC
MERGE(fc:Device {uid: randomUUID(),
                           name: row.`MEA ID`,
                           DOI: row.DOI,
                           date_added : "1111-11-11"
})
MERGE(mea:Component {uid: randomUUID(),
                          name: row.`MEA ID`,
                          DOI: row.DOI,
                          date_added : "1111-11-11"
})
// Other Components
MERGE(membrane:Component {uid: randomUUID(),
                          name: row.Mebrane,
                          DOI: row.DOI,
                          date_added: "1111-11-11"})
MERGE(plates:Component {uid: randomUUID(),
                        name: row.plates,
                        DOI: row.DOI,
                        date_added: "1111-11-11"})
MERGE(gdl:Component {uid: randomUUID(),
                     name: row.GDL,
                     DOI: row.DOI,
                     date_added: "1111-11-11"})
MERGE(anode:Component {uid: randomUUID(),
                     name: row.GDL,
                     DOI: row.DOI,
                     date_added: "1111-11-11"})

// FC-Manufacturing and MEA-Manufacturing
MERGE(fcfab:Manufacturing {uid: randomUUID(),
run_title: row.`MEA ID`,
DOI: row.DOI,
date_added : "1111-11-11"
})


MERGE(meafab:Manufacturing {uid: randomUUID(),
run_title: row.`MEA ID`,
DOI: row.DOI,
date_added : "1111-11-11"
})


// Labelling
MERGE(mea)-[:IS_A]->(EMMO_mea)
MERGE(fc)-[:IS_A]->(EMMO_fc)
MERGE(gdl)-[:IS_A]->(EMMO_gdl)
MERGE(bp)-[:IS_A]->(EMMO_bp)
MERGE(EMMO_membrane)<-[:IS_A]-(membrane)
MERGE(EMMO_meaas)<-[:IS_A]-(meafab)
MERGE(fcfab)-[:IS_A]->(EMMO_fcas)

//Processing
MERGE(meafab)<-[:HAS_PART]-(fcfab)
MERGE(meafab)-[:IS_PROCESS_OUTPUT]->(mea)
MERGE(membrane)-[:IS_PROCESS_INPUT]->(meafab)
MERGE(anode)-[:IS_PROCESS_INPUT]->(meafab)
