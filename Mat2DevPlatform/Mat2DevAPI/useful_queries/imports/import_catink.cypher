LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Mat2DevPlatform/Mat2DevAPI/data/jasna/CatInkFabrication.csv' AS row

MATCH (EMMO_ionomer:EMMO_Matter{EMMO__name: "AquivionD79-25BS"})<-[:IS_A]-(ionomer:Material),
      (ink:Material {name: row.`Run #`+"_ink"})-[:IS_A]-(:EMMO_Matter {EMMO__name: 'CatalystInk'}),
      (ionomer)<-[:HAS_PART]-(ink),
      (EMMO_carbonsupport:EMMO_Matter{EMMO__name: "AcetyleneBlack"})<-[:IS_A]-(carbon:Material),
      (carbon)<-[:HAS_PART]-(catalyst)-[:HAS_PART]-(ink),
      (EMMO_epoxy:EMMO_Matter{EMMO__name: 'Polyepoxide'}),
      (EMMO_cathode:EMMO_Matter{EMMO__name: 'Cathode'}),
      (EMMO_thickness:EMMO_Quantity{EMMO__name: 'Thickness'}),
      (EMMO_porosity:EMMO_Quantity{EMMO__name: 'Porosity'}),
      (EMMO_crackdensity:EMMO_Quantity{EMMO__name: 'CrackDensity'}),
      (EMMO_voidvol:EMMO_Quantity{EMMO__name: 'SpecificVolumeVoid'}),
      (EMMO_epoxyfilledvol:EMMO_Quantity{EMMO__name: 'SpecificVolumeSolid'}),
      (EMMO_ionomervol:EMMO_Quantity{EMMO__name: 'SpecificVolumeSolid'}),
      (EMMO_solidvol:EMMO_Quantity{EMMO__name: 'SpecificVolumeSolid'}),
      (EMMO_inaccessiblecarbonfraction:EMMO_Quantity{EMMO__name: 'InaccessiblePoreFraction'}),
      (EMMO_inaccessibleporefraction:EMMO_Quantity{EMMO__name: 'InaccassibleCarbonFraction'}),
      (EMMO_cclfab:EMMO_Process {EMMO__name: 'CCLManufacturing'}),
      (EMMO_powderdvs:EMMO_Process {EMMO__name: 'PowderDynamicVaporSorptionMeasurement'}),
      (EMMO_cldvs:EMMO_Process {EMMO__name: 'CatalystLayerDynamicVaporSorptionMeasurement'}),
      (EMMO_sem:EMMO_Process {EMMO__name: 'SEMImaging'}),
      (EMMO_tem:EMMO_Process {EMMO__name: 'TEMImaging'}),
      (EMMO_msp:EMMO_Process {EMMO__name: 'MethodOfStandardPorosimetry'}),
      (EMMO_rh:EMMO_Quantity {EMMO__name: 'RelativeHumidity'}),
      (EMMO_dvs:EMMO_Quantity {EMMO__name: 'DynamicVaporDesorption'}),
      (EMMO_dvds:EMMO_Quantity {EMMO__name: 'DynamicVaporSorption'}),
      (EMMO_ic:EMMO_Quantity{EMMO__name: "CatalystIonomerRatio"}),
      (EMMO_preparation:EMMO_Process {EMMO__name: 'SamplePreparation'})

// Process Nodes
MERGE(cclfab:Manufacturing {run_title: row.`Run #`,
                            uid: randomUUID(),
                           DOI: row.DOI
})
ON CREATE
SET cclfab.date_added = date()

MERGE(epoxy)-[:IS_A]->(EMMO_epoxy)
//Matter Nodes
MERGE(ccl:Material {name: row.`Run #`,
                    uid : randomUUID() })
ON CREATE
SET cclfab.date_added = date()


// Measurement nodes
MERGE(sem:Measurement{uid: randomUUID(),
                     date_added : date()
})
MERGE(keyence:Measurement{uid: randomUUID(),
                      date_added : date()
})
MERGE(thickness:Property{uid: randomUUID(),
                      date_added : date()
})
MERGE(porosity:Property{uid: randomUUID(),
                         date_added : date()
})
MERGE(voidvol:Property{uid: randomUUID(),
                        date_added : date()
})
MERGE(crackdensity:Property{uid: randomUUID(),
                       date_added : date()
})
MERGE(ccl)-[:IS_MEASUREMENT_INPUT]->(sem)-[:HAS_MEASUREMENT_OUTPUT]
  ->(thickness)-[:IS_A]->(EMMO_thickness)
MERGE(ccl)-[:HAS_PROPERTY{value: tofloat(row.`SEM thickness STD (µm)`), std: tofloat(row.`SEM thickness STD (µm)`)}]->(thickness)

MERGE(sem)-[:HAS_MEASUREMENT_OUTPUT]
  ->(porosity)-[:IS_A]->(EMMO_porosity)
MERGE(porosity)-[:DERIVED_FROM]->(thickness)
MERGE(ccl)-[:HAS_PROPERTY{value: tofloat(row.`Calculated porosity based on SEM thickness (%)`)}]->(porosity)

MERGE(sem)-[:HAS_MEASUREMENT_OUTPUT]
->(voidvol)-[:IS_A]->(EMMO_voidvol)
MERGE(voidvol)-[:DERIVED_FROM]->(thickness)
MERGE(ccl)-[:HAS_PROPERTY{value: tofloat(row.`Calculated PV based on SEM thickness (cm3/cm2geo)`)}]->(voidvol)

MERGE(ccl)-[:IS_MEASUREMENT_INPUT]->(keyence)-[:HAS_MEASUREMENT_OUTPUT]
->(crackdensity)-[:IS_A]->(EMMO_crackdensity)
MERGE(ccl)-[:HAS_PROPERTY{value: tofloat(row.`Keyence Crack density 400x mag (%)`)}]->(crackdensity)

FOREACH(x IN CASE WHEN row.`Densometer Porosity (%)` IS NOT NULL THEN [1] END |
  MERGE(densometer:Measurement{uid: randomUUID(),
                        date_added : date()})
  MERGE(dporosity:Property{uid: randomUUID(),
                              date_added : date()
  })
  MERGE(dsolidvolume:Property{uid: randomUUID(),
                           date_added : date()
  })
  MERGE(dthickness:Property{uid: randomUUID(),
                              date_added : date()
  })
  MERGE(dvoidvolume:Property{uid: randomUUID(),
                              date_added : date()
  })
  MERGE(ccl)-[:IS_MEASUREMENT_INPUT]->(densometer)-[:HAS_MEASUREMENT_OUTPUT]
  ->(dporosity)-[:IS_A]->(EMMO_porosity)
  MERGE(densometer)-[:HAS_MEASUREMENT_OUTPUT]
  ->(dthickness)-[:IS_A]->(EMMO_thickness)
  MERGE(densometer)-[:HAS_MEASUREMENT_OUTPUT]
  ->(dsolidvolume)-[:IS_A]->(EMMO_solidvol)
  MERGE(densometer)-[:HAS_MEASUREMENT_OUTPUT]
  ->(dvoidvolume)-[:IS_A]->(EMMO_voidvol)
  MERGE(ccl)-[:HAS_PROPERTY{value: tofloat(row.`Densometer PV (cm3/cm2geo)`)}]->(dvoidvolume)
  MERGE(ccl)-[:HAS_PROPERTY{value: tofloat(row.`Densometer solid volume (cm3/cm2 geo)`)}]->(dsolidvolume)
  MERGE(ccl)-[:HAS_PROPERTY{value: tofloat(row.`Densometer CL thickness (µm)`)}]->(dthickness)
  MERGE(ccl)-[:HAS_PROPERTY{value: tofloat(row.`Densometer Porosity (%)`)}]->(dporosity)
)

// DVS 50 RH
MERGE(dvs50:Measurement{uid: randomUUID(),
                      date_added : date()
})
MERGE(pdvs50:Property{uid: randomUUID(),
                         date_added : date()
})
MERGE(ink)-[:IS_MEASUREMENT_INPUT]->(dvs50)
MERGE(dvs50)-[:IS_A]->(EMMO_powderdvs)
MERGE(dvs50)-[:HAS_MEASUREMENT_OUTPUT]
->(pdvs50)-[:IS_A]->(EMMO_dvs)
CREATE(dvs50)-[:HAS_PARAMETER{value: 50}]->(:Parameter{uid : randomUUID()})-[:IS_A]->(EMMO_rh)
MERGE(ink)-[:HAS_PROPERTY{value: tofloat(row.`Powder DVS soprtion at 50%RH (% mass change/cm2geo)`)}]->(pdvs50)

// DVDS 50 RH
MERGE(dvds50:Measurement{uid: randomUUID(),
                        date_added : date()
})
MERGE(dvds50)-[:IS_A]->(EMMO_powderdvs)
MERGE(ink)-[:IS_MEASUREMENT_INPUT]->(dvds50)
MERGE(pdvds50:Property{uid: randomUUID(),
                      date_added : date()
})
MERGE(dvds50)-[:HAS_MEASUREMENT_OUTPUT]
->(pdvds50)-[:IS_A]->(EMMO_dvds)
CREATE(dvds50)-[:HAS_PARAMETER{value: 50}]->(:Parameter)-[:IS_A]->(EMMO_rh)
MERGE(ink)-[:HAS_PROPERTY{value: tofloat(row.`Powder DVS desoprtion at 50%RH (% mass change/cm2geo)`)}]->(pdvds50)


//DVS 95 RH
MERGE(dvs95:Measurement{uid: randomUUID(),
                         date_added : date()
})
MERGE(dvs95)-[:IS_A]->(EMMO_powderdvs)
MERGE(ink)-[:IS_MEASUREMENT_INPUT]->(dvs95)
MERGE(pdvs95:Property{uid: randomUUID(),
                       date_added : date()
})
MERGE(dvs95)-[:HAS_MEASUREMENT_OUTPUT]
->(pdvs95)-[:IS_A]->(EMMO_dvs)
CREATE(dvs95)-[:HAS_PARAMETER{value: 95}]->(:Parameter)-[:IS_A]->(EMMO_rh)
MERGE(ink)-[:HAS_PROPERTY{value: tofloat(row.`Powder DVS soprtion at 95%RH (% mass change/cm2geo)`)}]->(pdvs95)


//CL dvds 50 RH
FOREACH(x IN CASE WHEN row.`CL DVS desoprtion at 50%RH (% mass change/cm2geo)` IS NOT NULL THEN [1]
  END |
  MERGE(cldvds50:Measurement{uid:randomUUID(),
                           date_added:date()
  })
  MERGE(cldvds50)-[:IS_A]->(EMMO_cldvs)
  MERGE(ink)- [:IS_MEASUREMENT_INPUT] - >(dvds50)
  MERGE(clpdvds50:Property{uid:randomUUID(),
                          date_added:date()
  })
  MERGE(cldvds50)- [:HAS_MEASUREMENT_OUTPUT]
  - >(clpdvds50)- [:IS_A] - >(EMMO_dvds)
  CREATE(cldvds50)- [:HAS_PARAMETER{value:50}]- >(:Parameter)- [:IS_A] - >(EMMO_rh)
  MERGE(ink)-[:HAS_PROPERTY{value:TOFLOAT(row.`CL DVS desoprtion at 50%RH (% mass change/cm2geo)`)}]->(clpdvds50)

)

//CL DVS 50 RH
FOREACH(x IN CASE WHEN row.`CL DVS soprtion at 50%RH (% mass change/cm2geo)` IS NOT NULL THEN [1]
END |
MERGE(cldvs50:Measurement{uid:randomUUID(),
date_added:date()
})
MERGE(cldvs50)-[:IS_A]->(EMMO_cldvs)
MERGE(ink)- [:IS_MEASUREMENT_INPUT] - >(dvs50)
MERGE(clpdvs50:Property{uid:randomUUID(),
date_added:date()
})
MERGE(cldvs50)- [:HAS_MEASUREMENT_OUTPUT]
- >(clpdvs50)- [:IS_A] - >(EMMO_dvs)
CREATE(cldvs50)- [:HAS_PARAMETER{value:50}]- >(:Parameter)- [:IS_A] - >(EMMO_rh)
  MERGE(ink)-[:HAS_PROPERTY{value:TOFLOAT(row.`CL DVS soprtion at 50%RH (% mass change/cm2geo)`)}]->(clpdvs50)
)

//CL DVS 95 RH
FOREACH(x IN CASE WHEN row.`CL DVS soprtion at 95%RH (% mass change/cm2geo)` IS NOT NULL THEN [1]
  END |
  MERGE(tem:Measurement{uid:randomUUID(),
                           date_added: date(),
flag: "jasna"
  })
  MERGE(tem)-[:IS_A]->(EMMO_tem)
  MERGE(ink)- [:IS_MEASUREMENT_INPUT] - >(dvs95)
  MERGE(clpdvs95:Property{uid:randomUUID(),
                          date_added: date(),
                          flag: "jasna"
  })
  MERGE(cldvs95)- [:HAS_MEASUREMENT_OUTPUT]
  - >(clpdvs95)- [:IS_A] - >(EMMO_dvs)
  CREATE(cldvs95)- [:HAS_PARAMETER{value:95}]- >(:Parameter)- [:IS_A] - >(EMMO_rh)
  MERGE(ink)-[:HAS_PROPERTY{value:TOFLOAT(row.`CL DVS soprtion at 95%RH (% mass change/cm2geo)`)}]->(clpdvs95)

)

FOREACH(x IN CASE WHEN row.`TEM EDX Inaccessible pores (%)` IS NOT NULL THEN [1] END |
  MERGE(epoxy:Material {uid : randomUUID() ,
        date_added : date(),
        flag: "jasna"
        })
  MERGE(tem:Measurement{uid: randomUUID(),
        date_added : date(),
        flag: "jasna"
        })
  MERGE(temic:Property{uid: randomUUID(),
        date_added : date(),
        flag: "jasna"
        })
  MERGE(temionomervol:Property{uid: randomUUID(),
        date_added : date(),
        flag: "jasna"
        })
  MERGE(temporosity:Property{uid: randomUUID(),
        date_added : date(),
        flag: "jasna"
        })
  MERGE(temtotalporosity:Property{uid: randomUUID(),
        date_added : date(),
        flag: "jasna"
        })
  MERGE(temepoxy:Measurement{uid: randomUUID(),
        date_added : date(),
        flag: "jasna"
        })
  MERGE(preparation:Manufacturing{uid: randomUUID(),
        date_added : date(),
        flag: "jasna"
        })
  MERGE(preparation)-[:IS_A]->(EMMO_preparation)
  MERGE(temepoxy)-[:HAS_PART]->(preparation)
  MERGE(epoxy)-[:IS_MANUFACTURING_INPUT]->(preparation)
  MERGE(ccl)-[:IS_MANUFACTURING_INPUT]->(preparation)
  MERGE(epoxyccl:Material {uid : randomUUID() ,
        date_added : date(),
        flag: "jasna"
        })

  MERGE(preparation)-[:IS_MANUFACTURING_OUTPUT]->(epoxyccl)


  MERGE(temepoxyfilledporosity:Property{uid: randomUUID(),
        date_added : date(),
        flag: "jasna"
        })
  MERGE(teminaccessiblepores:Property{uid: randomUUID(),
        date_added : date(),
        flag: "jasna"
        })
  MERGE(teminaccessiblecarbon:Property{uid: randomUUID(),
        date_added : date(),
        flag: "jasna"
        })
  MERGE(temepoxyfilledvolume:Property{uid: randomUUID(),
        date_added : date(),
        flag: "jasna"
        })
  MERGE(temionomerthickness:Property{uid: randomUUID(),
        date_added : date(),
        flag: "jasna"
        })
  MERGE(ccl)- [:IS_MEASUREMENT_INPUT] - >(tem)-[:IS_A]->(EMMO_tem)
  MERGE(ccl)- [:IS_MEASUREMENT_INPUT] - >(temepoxy)-[:IS_A]->(EMMO_tem)
  MERGE(ccl)- [:HAS_PROPERTY{value: row.`I/C TEM measured `}] - >(temic)
  MERGE(temic)-[:IS_A]->(EMMO_ic)
  MERGE(ionomer)- [:HAS_PROPERTY{value: row.`Ionomer volume, cm3/cm2`}] - >(temionomervol)
  MERGE(temionomervol)-[:IS_A]->(EMMO_ionomervol)
  MERGE(ccl)- [:HAS_PROPERTY{value: row.`Theoretical porosity, based on TEM local thickness and target I/C`}] - >(temporosity)
  MERGE(temporosity)-[:IS_A]->(EMMO_porosity)
  MERGE(ccl)- [:HAS_PROPERTY{value: row.`TEM EDX Total porosity (%)`}] - >(temtotalporosity)
  MERGE(temtotalporosity)-[:IS_A]->(EMMO_porosity)
  MERGE(ccl)- [:HAS_PROPERTY{value: row.`TEM EDX Epoxy-filled porosity (%)`}] - >(temepoxyfilledporosity)
  MERGE(temepoxyfilledporosity)-[:IS_A]->(EMMO_porosity)
  MERGE(ccl)- [:HAS_PROPERTY{value: row.`TEM EDX Inaccessible pores (%)`}] - >(teminaccessiblepores)
  MERGE(teminaccessiblepores)-[:IS_A]->(EMMO_inaccessibleporefraction)
  MERGE(carbon)- [:HAS_PROPERTY{value: row.`TEM EDX % of Inaccessible Carbon (%)`}] - >(teminaccessiblecarbon)
  MERGE(teminaccessiblecarbon)-[:IS_A]->(EMMO_inaccessiblecarbonfraction)
  MERGE(epoxy)- [:HAS_PROPERTY{value: row.`TEM EDX Epoxy-filled Volume (cm3/cm2 geo)2`}] - >(temepoxyfilledvolume)
  MERGE(temepoxyfilledvolume)-[:IS_A]->(EMMO_epoxyfilledvol)
  MERGE(ionomer)- [:HAS_PROPERTY{value: row.`TEM EDX effective ionomer thickness deff wrt BET SA (nm)`, std: row.`TEM EDX effective ionomer thickness deff std dev (nm)`}] - >(temionomerthickness)
  MERGE(temionomerthickness)-[:IS_A]->(EMMO_thickness)





)


//Labeling
MERGE(ccl)-[:IS_A]->(EMMO_cathode)
MERGE(cclfab)-[:IS_A]->(EMMO_cclfab)
MERGE(sem)-[:IS_A]->(EMMO_sem)

// Processing
MERGE(ink)-[:IS_MANUFACTURING_INPUT]->(cclfab)
MERGE(cclfab)-[:IS_MANUFACTURING_OUTPUT]->(ccl)