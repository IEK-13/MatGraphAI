LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Mat2DevPlatform/Mat2DevAPI/data/CatInkFabrication.csv' AS row

MATCH (ink:Material {name: row.`Run #`})-[:IS_A]-(:EMMO_Material {EMMO__name: "CatalystInk"}),
      (EMMO_cathode:EMMO_Manufactured{EMMO__name: "Cathode"}),
      (EMMO_thickness:EMMO_Quantity{EMMO__name: "Thickness"}),
      (EMMO_porosity:EMMO_Quantity{EMMO__name: "Porosity"}),
      (EMMO_crackdensity:EMMO_Quantity{EMMO__name: "CrackDensity"}),
      (EMMO_voidvol:EMMO_Quantity{EMMO__name: "SpecificVolumeVoid"}),
      (EMMO_solidvol:EMMO_Quantity{EMMO__name: "SpecificVolumeSolid"}),
      (EMMO_cclfab:EMMO_Manufacturing {EMMO__name: "CCLManufacturing"})

// Process Nodes
MERGE(cclfab:Manufacturing {run_title: row.`Run #`,
                            uid: randomUUID(),
                           DOI: row.DOI,
                           date_added : "1111-11-11"
})


//Material Nodes
MERGE(ccl:Material {name: row.`Run #`,
                    uid : randomUUID() ,
                    date_added: "1111-11-11"})



// Measurement nodes
MERGE(sem:Measurement{uid: randomUUID(),
                     DOI: row.DOI,
                     date_added : "1111-11-11"
})
MERGE(keyence:Measurement{uid: randomUUID(),
                      DOI: row.DOI,
                      date_added : "1111-11-11"
})
MERGE(thickness:Property{uid: randomUUID(),
                      date_added : "1111-11-11"
})
MERGE(porosity:Property{uid: randomUUID(),
                         date_added : "1111-11-11"
})
MERGE(voidvol:Property{uid: randomUUID(),
                        date_added : "1111-11-11"
})
MERGE(crackdensity:Property{uid: randomUUID(),
                       date_added : "1111-11-11"
})
MERGE(ccl)-[:IS_MEASUREMENT_INPUT]->(sem)-[:YIELDS_FLOAT_PROPERTY{
  value: TOFLOAT(row.`SEM thickness STD (µm)`), std: TOFLOAT(row.`SEM thickness STD (µm)`)}]
  ->(thickness)-[:IS_A]->(EMMO_thickness)

MERGE(sem)-[:YIELDS_FLOAT_PROPERTY{value: TOFLOAT(row.`Calculated porosity based on SEM thickness (%)`)}]
  ->(porosity)-[:IS_A]->(EMMO_porosity)
MERGE(porosity)-[:DERIVED_FROM]->(thickness)

MERGE(sem)-[:YIELDS_FLOAT_PROPERTY{value: TOFLOAT(row.`Calculated PV based on SEM thickness (cm3/cm2geo)`)}]
->(voidvol)-[:IS_A]->(EMMO_voidvol)
MERGE(voidvol)-[:DERIVED_FROM]->(thickness)

MERGE(ccl)-[:IS_MEASUREMENT_INPUT]->(keyence)-[:YIELDS_FLOAT_PROPERTY{
  value: TOFLOAT(row.`Keyence Crack density 400x mag (%)`)}]
->(crackdensity)-[:IS_A]->(EMMO_crackdensity)

FOREACH(x IN CASE WHEN row.`Densometer Porosity (%)` IS NOT NULL THEN [1] END |
  MERGE(densometer:Measurement{uid: randomUUID(),
                        date_added : "1111-11-11"})
  MERGE(dporosity:Property{uid: randomUUID(),
                              date_added : "1111-11-11"
  })
  MERGE(dsolidvolume:Property{uid: randomUUID(),
                           date_added : "1111-11-11"
  })
  MERGE(dthickness:Property{uid: randomUUID(),
                              date_added : "1111-11-11"
  })
  MERGE(dvoidvolume:Property{uid: randomUUID(),
                              date_added : "1111-11-11"
  })
  MERGE(ccl)-[:IS_MEASUREMENT_INPUT]->(densometer)-[:YIELDS_FLOAT_PROPERTY{
    value: TOFLOAT(row.`Densometer Porosity (%)`)}]
  ->(dporosity)-[:IS_A]->(EMMO_porosity)
  MERGE(densometer)-[:YIELDS_FLOAT_PROPERTY{value: TOFLOAT(row.`Densometer CL thickness (µm)`)}]
  ->(dthickness)-[:IS_A]->(EMMO_thickness)
  MERGE(densometer)-[:YIELDS_FLOAT_PROPERTY{value: TOFLOAT(row.`Densometer solid volume (cm3/cm2 geo)`)}]
  ->(dsolidvolume)-[:IS_A]->(EMMO_solidvol)
  MERGE(densometer)-[:YIELDS_FLOAT_PROPERTY{value: TOFLOAT(row.`Densometer PV (cm3/cm2geo)`)}]
  ->(dvoidvolume)-[:IS_A]->(EMMO_voidvol)
)

//Labeling
MERGE(ccl)-[:IS_A]->(EMMO_cathode)
MERGE(cclfab)-[:IS_A]->(EMMO_cclfab)

// Processing
MERGE(ink)-[:IS_MANUFACTURING_INPUT]->(cclfab)
MERGE(cclfab)-[:IS_MANUFACTURING_OUTPUT]->(ccl)