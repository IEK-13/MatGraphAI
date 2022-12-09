LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Mat2DevPlatform/Mat2DevAPI/data/FuelCellFabrication.csv' AS row

MATCH (EMMO_fcas:EMMO_Manufacturing {EMMO__name: "FuelCellAssembly"}),
      (EMMO_meaas:EMMO_Manufacturing {EMMO__name: "CCMManufacturing"}),
      (EMMO_membrane:EMMO_Manufactured{EMMO__name: "Membrane"}),
      (EMMO_mea:EMMO_Manufactured{EMMO__name: "CCM"}),
      (EMMO_fc:EMMO_Manufactured{EMMO__name: "FuelCell"}),
      (EMMO_bp:EMMO_Manufactured{EMMO__name: "BipolarPlate"}),
      (EMMO_ionomer:EMMO_Material{EMMO__name: "AquivionD79-25BS"}),
      (EMMO_anode:EMMO_Manufactured{EMMO__name: "Anode"}),
      (EMMO_catalyst:EMMO_Material{EMMO__name: "F50E-HT"}),
      (EMMO_bp:EMMO_Manufactured{EMMO__name: "BipolarPlate"}),
      (EMMO_PTFE:EMMO_Material{EMMO__name: "PTFE"}),
      (EMMO_ETFE:EMMO_Material{EMMO__name: "ETFE"}),
      (EMMO_ink:EMMO_Material{EMMO__name: "CatalystInk"}),
      (EMMO_gdl:EMMO_Manufactured{EMMO__name: "GasDiffusionLayer"}),
      (EMMO_station:EMMO_Manufactured{EMMO__name: "Station"})





// MEA and FC
MERGE(fc:Device {uid: randomUUID(),
                           name: row.`MEA ID`,
                           DOI: row.DOI,
                           date_added : "1111-11-11"
})
MERGE(catink:Material {uid: randomUUID(),
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
                          name: row.Membrane,
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
MERGE(station:Component {uid: randomUUID(),
                     name: row.Station,
                     DOI: row.DOI,
                     date_added: "1111-11-11"})
MERGE(anode:Component {uid: randomUUID(),
                     name: row.Anode,
                     DOI: row.DOI,
                     date_added: "1111-11-11"})

MERGE(ionomer:Material {uid: randomUUID(),
                       name: row.Ionomer,
                       DOI: row.DOI,
                       date_added: "1111-11-11"})
MERGE(catalyst:Material {uid: randomUUID(),
                         name: row.Catalyst,
                         DOI: row.DOI,
                         date_added: "1111-11-11"})
MERGE(coatingsubstrate:Material {uid: randomUUID(),
                          name: row.`Coating substrate`,
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

MERGE(inkfab:Manufacturing {uid: randomUUID(),
                            run_title: row.`MEA ID`,
                            DOI: row.DOI,
                            date_added : "1111-11-11"
})


// Labelling
MERGE(EMMO_meaas)<-[:IS_A]-(meafab)
MERGE(fcfab)-[:IS_A]->(EMMO_fcas)

MERGE(mea)-[:IS_A]->(EMMO_mea)
MERGE(fc)-[:IS_A]->(EMMO_fc)
MERGE(gdl)-[:IS_A]->(EMMO_gdl)
MERGE(bp)-[:IS_A]->(EMMO_bp)
MERGE(ionomer)-[:IS_A]->(EMMO_ionomer)
MERGE(catalyst)-[:IS_A]->(EMMO_catalyst)
MERGE(anode)-[:IS_A]->(EMMO_anode)
MERGE(membrane)-[:IS_A]->(EMMO_membrane)
MERGE(station)-[:IS_A]->(EMMO_station)
MERGE(ETFE)-[:IS_A]->(EMMO_PTFE)
MERGE(ink)-[:IS_A]->(EMMO_ink)


//Processing
MERGE(meafab)<-[:HAS_PART]-(fcfab)
MERGE(inkfab)<-[:HAS_PART]-(meafab)

MERGE(catalyst)-[:IS_PROCESS_INPUT]->(inkfab)
MERGE(ionomer)-[:IS_PROCESS_INPUT]->(inkfab)
MERGE(inkfab)-[:IS_PROCESS_OUTPUT]->(catink)

MERGE(meafab)-[:IS_PROCESS_OUTPUT]->(mea)
MERGE(membrane)-[:IS_PROCESS_INPUT]->(meafab)
MERGE(anode)-[:IS_PROCESS_INPUT]->(meafab)
MERGE(catink)-[:IS_PROCESS_INPUT]->(meafab)
MERGE(coatingsubstrate)-[:IS_PROCESS_INPUT]->(meafab)


MERGE(plates)-[:IS_PROCESS_INPUT]->(fcfab)
MERGE(mea)-[:IS_PROCESS_INPUT]->(fcfab)
MERGE(gdl)-[:IS_PROCESS_INPUT]->(fcfab)
MERGE(station)-[:IS_PROCESS_INPUT]->(fcfab)
MERGE(fcfab)-[:IS_PROCESS_OUTPUT]->(fc)



