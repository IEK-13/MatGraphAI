LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Mat2DevPlatform/Mat2DevAPI/data/CatInkFabrication.csv' AS row

MATCH (ink:Material {name: row.`Run #`})-[:IS_A]-(:EMMO_Matter {EMMO__name: 'CatalystInk'}),
      (EMMO_cathode:EMMO_Matter{EMMO__name: 'Cathode'}),
      (EMMO_thickness:EMMO_Quantity{EMMO__name: 'Thickness'}),
      (EMMO_porosity:EMMO_Quantity{EMMO__name: 'Porosity'}),
      (EMMO_crackdensity:EMMO_Quantity{EMMO__name: 'CrackDensity'}),
      (EMMO_voidvol:EMMO_Quantity{EMMO__name: 'SpecificVolumeVoid'}),
      (EMMO_solidvol:EMMO_Quantity{EMMO__name: 'SpecificVolumeSolid'}),
      (EMMO_cclfab:EMMO_Process {EMMO__name: 'CCLManufacturing'}),
      (EMMO_powderdvs:EMMO_Process {EMMO__name: 'PowderDynamicVaporSorption'}),
      (EMMO_cldvs:EMMO_Process {EMMO__name: 'CatalystLayerDynamicVaporSorption'}),
      (EMMO_sem:EMMO_Process {EMMO__name: 'SEMImaging'}),
      (EMMO_msp:EMMO_Process {EMMO__name: 'MethodOfStandardPorosimetry'}),
      (EMMO_rh:EMMO_Quantity {EMMO__name: 'RelativeHumidity'}),
      (EMMO_dvs:EMMO_Quantity {EMMO__name: 'DynamicVaporDesorption'}),
      (EMMO_dvds:EMMO_Quantity {EMMO__name: 'DynamicVaporSorption'})

// Process Nodes
MERGE(cclfab:Manufacturing {run_title: row.`Run #`,
                            uid: randomUUID(),
                           DOI: row.DOI,
                           date_added : '1111-11-11'
})


//Material Nodes
MERGE(ccl:Material {name: row.`Run #`,
                    uid : randomUUID() ,
                    date_added: '1111-11-11'})



// Measurement nodes
MERGE(sem:Measurement{uid: randomUUID(),
                     date_added : '1111-11-11'
})
MERGE(keyence:Measurement{uid: randomUUID(),
                      date_added : '1111-11-11'
})
MERGE(thickness:Property{uid: randomUUID(),
                      date_added : '1111-11-11'
})
MERGE(porosity:Property{uid: randomUUID(),
                         date_added : '1111-11-11'
})
MERGE(voidvol:Property{uid: randomUUID(),
                        date_added : '1111-11-11'
})
MERGE(crackdensity:Property{uid: randomUUID(),
                       date_added : '1111-11-11'
})
MERGE(ccl)-[:IS_MEASUREMENT_INPUT]->(sem)-[:YIELDS_FLOAT_PROPERTY{
  value: tofloat(row.`SEM thickness STD (µm)`), std: tofloat(row.`SEM thickness STD (µm)`)}]
  ->(thickness)-[:IS_A]->(EMMO_thickness)
MERGE(ccl)-[:hasProperty]->(thickness)

MERGE(sem)-[:YIELDS_FLOAT_PROPERTY{value: tofloat(row.`Calculated porosity based on SEM thickness (%)`)}]
  ->(porosity)-[:IS_A]->(EMMO_porosity)
MERGE(porosity)-[:DERIVED_FROM]->(thickness)
MERGE(ccl)-[:hasProperty]->(porosity)

MERGE(sem)-[:YIELDS_FLOAT_PROPERTY{value: tofloat(row.`Calculated PV based on SEM thickness (cm3/cm2geo)`)}]
->(voidvol)-[:IS_A]->(EMMO_voidvol)
MERGE(voidvol)-[:DERIVED_FROM]->(thickness)
MERGE(ccl)-[:hasProperty]->(voidvol)

MERGE(ccl)-[:IS_MEASUREMENT_INPUT]->(keyence)-[:YIELDS_FLOAT_PROPERTY{
  value: tofloat(row.`Keyence Crack density 400x mag (%)`)}]
->(crackdensity)-[:IS_A]->(EMMO_crackdensity)
MERGE(ccl)-[:hasProperty]->(crackdensity)

FOREACH(x IN CASE WHEN row.`Densometer Porosity (%)` IS NOT NULL THEN [1] END |
  MERGE(densometer:Measurement{uid: randomUUID(),
                        date_added : '1111-11-11'})
  MERGE(dporosity:Property{uid: randomUUID(),
                              date_added : '1111-11-11'
  })
  MERGE(dsolidvolume:Property{uid: randomUUID(),
                           date_added : '1111-11-11'
  })
  MERGE(dthickness:Property{uid: randomUUID(),
                              date_added : '1111-11-11'
  })
  MERGE(dvoidvolume:Property{uid: randomUUID(),
                              date_added : '1111-11-11'
  })
  MERGE(ccl)-[:IS_MEASUREMENT_INPUT]->(densometer)-[:YIELDS_FLOAT_PROPERTY{
    value: tofloat(row.`Densometer Porosity (%)`)}]
  ->(dporosity)-[:IS_A]->(EMMO_porosity)
  MERGE(densometer)-[:YIELDS_FLOAT_PROPERTY{value: tofloat(row.`Densometer CL thickness (µm)`)}]
  ->(dthickness)-[:IS_A]->(EMMO_thickness)
  MERGE(densometer)-[:YIELDS_FLOAT_PROPERTY{value: tofloat(row.`Densometer solid volume (cm3/cm2 geo)`)}]
  ->(dsolidvolume)-[:IS_A]->(EMMO_solidvol)
  MERGE(densometer)-[:YIELDS_FLOAT_PROPERTY{value: tofloat(row.`Densometer PV (cm3/cm2geo)`)}]
  ->(dvoidvolume)-[:IS_A]->(EMMO_voidvol)
  MERGE(ccl)-[:hasProperty]->(dvoidvolume)
  MERGE(ccl)-[:hasProperty]->(dsolidvolume)
  MERGE(ccl)-[:hasProperty]->(dthickness)
  MERGE(ccl)-[:hasProperty]->(dporosity)
)

// DVS 50 RH
MERGE(dvs50:Measurement{uid: randomUUID(),
                      date_added : '1111-11-11'
})
MERGE(pdvs50:Property{uid: randomUUID(),
                         date_added : '1111-11-11'
})
MERGE(ink)-[:IS_MEASUREMENT_INPUT]->(dvs50)
MERGE(dvs50)-[:IS_A]->(EMMO_powderdvs)
MERGE(dvs50)-[:YIELDS_FLOAT_PROPERTY{value: tofloat(row.`Powder DVS soprtion at 50%RH (% mass change/cm2geo)`)}]
->(pdvs50)-[:IS_A]->(EMMO_dvs)
CREATE(dvs50)-[:HAS_FLOAT_PARAMETER{value: 50}]->(:Parameter)-[:IS_A]->(EMMO_rh)
MERGE(ink)-[:hasProperty]->(pdvs50)

// DVDS 50 RH
MERGE(dvds50:Measurement{uid: randomUUID(),
                        date_added : '1111-11-11'
})
MERGE(dvds50)-[:IS_A]->(EMMO_powderdvs)
MERGE(ink)-[:IS_MEASUREMENT_INPUT]->(dvds50)
MERGE(pdvds50:Property{uid: randomUUID(),
                      date_added : '1111-11-11'
})
MERGE(dvds50)-[:YIELDS_FLOAT_PROPERTY{value: tofloat(row.`Powder DVS desoprtion at 50%RH (% mass change/cm2geo)`)}]
->(pdvds50)-[:IS_A]->(EMMO_dvds)
CREATE(dvds50)-[:HAS_FLOAT_PARAMETER{value: 50}]->(:Parameter)-[:IS_A]->(EMMO_rh)
MERGE(ink)-[:hasProperty]->(pdvds50)


//DVS 95 RH
MERGE(dvs95:Measurement{uid: randomUUID(),
                         date_added : '1111-11-11'
})
MERGE(dvs95)-[:IS_A]->(EMMO_powderdvs)
MERGE(ink)-[:IS_MEASUREMENT_INPUT]->(dvs95)
MERGE(pdvs95:Property{uid: randomUUID(),
                       date_added : '1111-11-11'
})
MERGE(dvs95)-[:YIELDS_FLOAT_PROPERTY{value: tofloat(row.`Powder DVS soprtion at 95%RH (% mass change/cm2geo)`)}]
->(pdvs95)-[:IS_A]->(EMMO_dvs)
CREATE(dvs95)-[:HAS_FLOAT_PARAMETER{value: 95}]->(:Parameter)-[:IS_A]->(EMMO_rh)

//CL dvds 50 RH
FOREACH(x IN CASE WHEN row.`CL DVS desoprtion at 50%RH (% mass change/cm2geo)` IS NOT NULL THEN [1]
  END |
  MERGE(cldvds50:Measurement{uid:randomUUID(),
                           date_added:"1111-11-11"
  })
  MERGE(cldvds50)-[:IS_A]->(EMMO_cldvs)
  MERGE(ink)- [:IS_MEASUREMENT_INPUT] - >(dvds50)
  MERGE(clpdvds50:Property{uid:randomUUID(),
                          date_added:"1111-11-11"
  })
  MERGE(cldvds50)- [:YIELDS_FLOAT_PROPERTY{value:TOFLOAT(row.`CL DVS desoprtion at 50%RH (% mass change/cm2geo)`)}]
  - >(clpdvds50)- [:IS_A] - >(EMMO_dvds)
  CREATE(cldvds50)- [:HAS_FLOAT_PARAMETER{value:50}]- >(:Parameter)- [:IS_A] - >(EMMO_rh)
)

//CL DVS 50 RH
FOREACH(x IN CASE WHEN row.`CL DVS soprtion at 50%RH (% mass change/cm2geo)` IS NOT NULL THEN [1]
END |
MERGE(cldvs50:Measurement{uid:randomUUID(),
date_added:"1111-11-11"
})
MERGE(cldvs50)-[:IS_A]->(EMMO_cldvs)
MERGE(ink)- [:IS_MEASUREMENT_INPUT] - >(dvs50)
MERGE(clpdvs50:Property{uid:randomUUID(),
date_added:"1111-11-11"
})
MERGE(cldvs50)- [:YIELDS_FLOAT_PROPERTY{value:TOFLOAT(row.`CL DVS soprtion at 50%RH (% mass change/cm2geo)`)}]
- >(clpdvs50)- [:IS_A] - >(EMMO_dvs)
CREATE(cldvs50)- [:HAS_FLOAT_PARAMETER{value:50}]- >(:Parameter)- [:IS_A] - >(EMMO_rh)
)

//CL DVS 95 RH
FOREACH(x IN CASE WHEN row.`CL DVS soprtion at 95%RH (% mass change/cm2geo)` IS NOT NULL THEN [1]
  END |
  MERGE(cldvs95:Measurement{uid:randomUUID(),
                           date_added:"1111-11-11"
  })
  MERGE(cldvs95)-[:IS_A]->(EMMO_cldvs)
  MERGE(ink)- [:IS_MEASUREMENT_INPUT] - >(dvs95)
  MERGE(clpdvs95:Property{uid:randomUUID(),
                          date_added:"1111-11-11"
  })
  MERGE(cldvs95)- [:YIELDS_FLOAT_PROPERTY{value:TOFLOAT(row.`CL DVS soprtion at 95%RH (% mass change/cm2geo)`)}]
  - >(clpdvs95)- [:IS_A] - >(EMMO_dvs)
  CREATE(cldvs95)- [:HAS_FLOAT_PARAMETER{value:95}]- >(:Parameter)- [:IS_A] - >(EMMO_rh)
)



//Labeling
MERGE(ccl)-[:IS_A]->(EMMO_cathode)
MERGE(cclfab)-[:IS_A]->(EMMO_cclfab)
MERGE(sem)-[:IS_A]->(EMMO_sem)

// Processing
MERGE(ink)-[:IS_MANUFACTURING_INPUT]->(cclfab)
MERGE(cclfab)-[:IS_MANUFACTURING_OUTPUT]->(ccl)