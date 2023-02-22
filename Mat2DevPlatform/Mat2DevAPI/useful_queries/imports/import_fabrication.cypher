LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Mat2DevPlatform/Mat2DevAPI/data/jasna/FuelCellFabrication.csv' AS row

MATCH (EMMO_fcas:EMMO_Process {EMMO__name: "FuelCellAssembly"}),
      (EMMO_fcfab:EMMO_Process {EMMO__name: "FuelCellManufacturing"}),
      (EMMO_meaas:EMMO_Process {EMMO__name: "CCMManufacturing"}),
      (EMMO_membrane:EMMO_Matter{EMMO__name: "Membrane"}),
      (EMMO_mea:EMMO_Matter{EMMO__name: "CCM"}),
      (EMMO_fc:EMMO_Matter{EMMO__name: "FuelCell"}),
      (EMMO_bp:EMMO_Matter{EMMO__name: "BipolarPlate"}),
      (EMMO_carbonsupport:EMMO_Matter{EMMO__name: "AcetyleneBlack"}),
      (EMMO_ionomer:EMMO_Matter{EMMO__name: "AquivionD79-25BS"}),
      (EMMO_anode:EMMO_Matter{EMMO__name: "Anode"}),
      (EMMO_catalyst:EMMO_Matter{EMMO__name: "F50E-HT"}),
      (EMMO_bp:EMMO_Matter{EMMO__name: "BipolarPlate"}),
      (EMMO_PTFE:EMMO_Matter{EMMO__name: "PTFE"}),
      (EMMO_ink:EMMO_Matter{EMMO__name: "CatalystInk"}),
      (EMMO_gdl:EMMO_Matter{EMMO__name: "GasDiffusionLayer"}),
      (EMMO_station:EMMO_Matter{EMMO__name: "Station"}),
      (EMMO_inkfab:EMMO_Process{EMMO__name: "CatalystInkManufacturing"}),
      (EMMO_loading:EMMO_Quantity{EMMO__name: "CatalystLoading"}),
      (EMMO_ew:EMMO_Quantity{EMMO__name: "EquivalentWeight"}),
      (EMMO_ic:EMMO_Quantity{EMMO__name: "CatalystIonomerRatio"}),
      (EMMO_mill:EMMO_Quantity{EMMO__name: "DryMillingTime"}),
      (EMMO_dt:EMMO_Quantity{EMMO__name: "DryingTemperature"})

// MEA and FC
MERGE(fc:Device {name: row.`Run #`+"FuelCell",
                 date_added : date()
})
  ON CREATE
  SET fc.uid = randomUUID()

MERGE(catink:Material {name: row.`Run #`+"_ink",
     date_added : date(),
     flag: "jasna"
})
  ON CREATE
  SET catink.uid = randomUUID()

MERGE(mea:Component {uid: randomUUID(),
                     name: row.`Run #`,
      date_added : date(),
      flag: "jasna"
})
// Other Components
MERGE(membrane:Material {name: row.Membrane,
      date_added : date(),
      flag: "jasna"
})
  ON CREATE
  SET membrane.uid = randomUUID()

MERGE(bp:Component {name: row.plates,
      date_added : date(),
      flag: "jasna"
      })
  ON CREATE
  SET bp.uid = randomUUID()

MERGE(gdl:Component {name: row.GDL,
      date_added : date(),
      flag: "jasna"
      })
  ON CREATE
  SET gdl.uid = randomUUID()

MERGE(station:Component {name: row.Station,
      date_added : date(),
      flag: "jasna"
      })
  ON CREATE
  SET station.uid = randomUUID()

MERGE(anode:Material {name: row.Anode,
      date_added : date(),
      flag: "jasna"
      })
  ON CREATE
  SET anode.uid = randomUUID()

MERGE(ionomer:Material {name: row.Ionomer,
      date_added : date(),
      flag: "jasna"
      })
  ON CREATE
  SET ionomer.uid = randomUUID()

MERGE(catalyst:Material {name: row.Catalyst,
      date_added : date(),
      flag: "jasna"
      })
  ON CREATE
  SET catalyst.uid = randomUUID()

MERGE(carbonsupport:Material {name: row.`Catalyst`+"support",
      date_added : date(),
      flag: "jasna"
      })
  ON CREATE
  SET carbonsupport.uid = randomUUID()

MERGE(carbonsupport)<-[:HAS_PART]-(catalyst)
MERGE(carbonsupport)-[:IS_A]->(EMMO_carbonsupport)


MERGE(coatingsubstrate:Material {name: row.`Coating substrate`,
      date_added : date(),
      flag: "jasna"
      })
  ON CREATE
  SET coatingsubstrate.uid = randomUUID()



// FC-Manufacturing and MEA-Manufacturing
MERGE(fcfab:Manufacturing {uid: randomUUID(),
      run_title: row.`Run #` + "_FuellCellManufacturing",
      DOI: row.DOI,
      date_added : date(),
      flag: "jasna"
      })

MERGE(fcass:Manufacturing {uid: randomUUID(),
      run_title: row.`Run #`+"_FuelCellAssembly",
      DOI: row.DOI,
      date_added : date(),
      flag: "jasna"
      })


MERGE(meafab:Manufacturing {uid: randomUUID(),
      run_title: row.`Run #`+"_MEAManufacturing",
      DOI: row.DOI,
      date_added : date(),
      flag: "jasna"
      })

MERGE(inkfab:Manufacturing {run_title: row.`Run #`+ "_InkFabrication",
      date_added : date(),
      flag: "jasna"
      })
  ON CREATE
  SET inkfab.uid = randomUUID()


// Labelling
MERGE(EMMO_meaas)<-[:IS_A]-(meafab)
MERGE(fcass)-[:IS_A]->(EMMO_fcas)
MERGE(inkfab)-[:IS_A]->(EMMO_inkfab)
MERGE(fcfab)-[:IS_A]->(EMMO_fcfab)


MERGE(mea)-[:IS_A]->(EMMO_mea)
MERGE(fc)-[:IS_A]->(EMMO_fc)
MERGE(gdl)-[:IS_A]->(EMMO_gdl)
MERGE(bp)-[:IS_A]->(EMMO_bp)
MERGE(ionomer)-[:IS_A]->(EMMO_ionomer)
MERGE(catalyst)-[:IS_A]->(EMMO_catalyst)
MERGE(anode)-[:IS_A]->(EMMO_anode)
MERGE(membrane)-[:IS_A]->(EMMO_membrane)
MERGE(station)-[:IS_A]->(EMMO_station)
MERGE(coatingsubstrate)-[:IS_A]->(EMMO_PTFE)
MERGE(catink)-[:IS_A]->(EMMO_ink)


//Processing
MERGE(fcfab)-[:HAS_PART]->(fcass)
MERGE(fcfab)-[:HAS_PART]->(meafab)
MERGE(fcfab)-[:HAS_PART]->(inkfab)

MERGE(meafab)-[:FOLLOWED_BY]->(fcass)
MERGE(inkfab)-[:FOLLOWED_BY]->(meafab)

MERGE(catalyst)-[:IS_MANUFACTURING_INPUT]->(inkfab)
MERGE(ionomer)-[:IS_MANUFACTURING_INPUT]->(inkfab)
MERGE(inkfab)-[:IS_MANUFACTURING_OUTPUT]->(catink)

MERGE(meafab)-[:IS_MANUFACTURING_OUTPUT]->(mea)
MERGE(membrane)-[:IS_MANUFACTURING_INPUT]->(meafab)
MERGE(anode)-[:IS_MANUFACTURING_INPUT]->(meafab)
MERGE(catink)-[:IS_MANUFACTURING_INPUT]->(meafab)
MERGE(coatingsubstrate)-[:IS_MANUFACTURING_INPUT]->(meafab)


MERGE(bp)-[:IS_MANUFACTURING_INPUT]->(fcass)
MERGE(mea)-[:IS_MANUFACTURING_INPUT]->(fcass)
MERGE(gdl)-[:IS_MANUFACTURING_INPUT]->(meafab)
MERGE(station)-[:IS_MANUFACTURING_INPUT]->(fcass)
MERGE(fcass)-[:IS_MANUFACTURING_OUTPUT]->(fc)

// Composition
MERGE(ink)-[:HAS_PART]->(catalyst)
MERGE(ink)-[:HAS_PART]->(ionomer)

MERGE(mea)-[:HAS_PART]->(gdl)
MERGE(mea)-[:HAS_PART]->(ink)
MERGE(mea)-[:HAS_PART]->(membrane)
MERGE(mea)-[:HAS_PART]->(anode)

MERGE(fc)-[:HAS_PART]->(mea)
MERGE(fc)-[:HAS_PART]->(station)
MERGE(fc)-[:HAS_PART]->(bp)

MERGE(catink)-[:HAS_PART]->(ionomer)
MERGE(catink)-[:HAS_PART]->(catalyst)

MERGE(catalyst)-[:HAS_PART]->(carbonsupport)




// Properties

MERGE(loading:Measurement{uid: randomUUID(),
                          DOI: row.DOI,
                          date_added : date()
})
MERGE(ploading:Property{uid: randomUUID(),
                          DOI: row.DOI,
                          date_added : date()
})
MERGE(mea)-[:IS_MEASUREMENT_INPUT]->(loading)-[:HAS_MEASUREMENT_OUTPUT]->(ploading)-[:IS_A]->(EMMO_loading)
MERGE(mea)-[:HAS_PROPERTY{
  value: TOFLOAT(row.`Pt loading (mg/cm2geo)`)}]->(ploading)

MERGE(ic:Measurement{uid: row.`Run #`,
                     DOI: row.`Run #`,
                     date_added : date()
})
SET ic.uid = randomUUID()
SET ic.DOI = row.DOI
MERGE(pic:Property{uid: row.`Run #`,
                        DOI: row.`Run #`,
                        date_added : date()
})
SET pic.uid = randomUUID()
SET pic.DOI = row.DOI

MERGE(catink)-[:IS_MEASUREMENT_INPUT]->(ic)-[:HAS_MEASUREMENT_OUTPUT]->(pic)-[:IS_A]->(EMMO_ic)
MERGE(catink)-[:HAS_PROPERTY{
  value: TOFLOAT(row.`I/C`)}]->(pic)


MERGE(ew:Measurement{uid: row.EW,
                     date_added : date()
})

SET ew.uid = randomUUID()
MERGE(pew:Property{uid: row.EW,
                     date_added : date()
})

SET pew.uid = randomUUID()
MERGE(ionomer)-[:IS_MEASUREMENT_INPUT]->(ew)-[:HAS_MEASUREMENT_OUTPUT]->(pew)-[:IS_A]->(EMMO_ew)
MERGE(ionomer)-[:HAS_PROPERTY{
  value: TOFLOAT(row.`EW`)}]->(pew)

// Paraneters

MERGE(inkfab)-[:HAS_PARAMETER{value: TOFLOAT(row.`Drymill time (hrs)`)}]->(:Parameter)-[:IS_A]->(EMMO_mill)

MERGE(meafab)-[:HAS_PARAMETER{value: TOFLOAT(row.`Drying temp (deg C)`)}]->(:Parameter)-[:IS_A]->(EMMO_dt)




