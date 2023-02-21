LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Mat2DevPlatform/Mat2DevAPI/data/lukas/DLS/IrO2-15wt-ic013-1Prop086-066ml_DLS.csv' AS row

MATCH(researcher:Researcher {first_name: row.Researcher})
MATCH(material:Material {name:row.Material})
MATCH(emmo_measurement:EMMO_Process {EMMO__name: row.Ontology})

MATCH(emmo_hydrodynamicdiameter:EMMO_Quantity {EMMO__name: "HydrodynamicDiameter"})
MATCH(emmo_averagehydrodynamicdiameter:EMMO_Quantity {EMMO__name: "AverageHydrodynamicDiameter"})
MATCH(emmo_hydrodynamicvolume:EMMO_Quantity {EMMO__name: "HydrodynamicVolume"})
MATCH(emmo_intensity:EMMO_Quantity {EMMO__name: "Intensity"})
MATCH(emmo_pdi:EMMO_Quantity {EMMO__name: "PolydispersityIndex"})



MERGE(measurement:Measurement {PIDA: row.PIDA,
                               flag: "findich",
                               date_added: "02/21/23",
                               experiment_start: row.`Measurement Data and Time`,
                               experiment_end: row.`Measurement Data and Time`,
                               instrument: row.Instrument})
  ON CREATE
  SET measurement.uid = randomUUID()

MERGE(material)-[:IS_MEASUREMENT_INPUT]->(measurement)
MERGE(measurement)-[:BY]->(researcher)

MERGE(hydrodynamicdiameter:Property {name: "hydrodynamicdiameter"+row.PIDA, 
                                     flag: "findich",
                                     date_added: "02/21/23"})
  ON CREATE
  SET hydrodynamicdiameter.uid = randomUUID()
MERGE(measurement)-[:HAS_MEASUREMENT_OUTPUT {value: apoc.convert.toList(toFloat(row.sizes))}]->(hydrodynamicdiameter)
MERGE(hydrodynamicdiameter)-[:IS_A]->(emmo_hydrodynamicdiameter)

MERGE(averagehydrodynamicdiameter:Property {name: "averagehydrodynamicdiameter"+row.PIDA,
                                            flag: "findich",
                                            date_added: "02/21/23"})
  ON CREATE
  SET averagehydrodynamicdiameter.uid = randomUUID()
MERGE(measurement)-[:HAS_MEASUREMENT_OUTPUT {value: toFloat(row.`Z-Average (d.nm)`)}]->(averagehydrodynamicdiameter)
MERGE(averagehydrodynamicdiameter)-[:IS_A]->(emmo_averagehydrodynamicdiameter)

MERGE(hydrodynamicvolume:Property {name: "hydrodynamicvolume"+row.PIDA,
                                   flag: "findich",
                                   date_added: "02/21/23"})
  ON CREATE
  SET hydrodynamicvolume.uid = randomUUID()
MERGE(measurement)-[:HAS_MEASUREMENT_OUTPUT {value: apoc.convert.toList(toFloat(row.volumes))}]->(hydrodynamicvolume)
MERGE(hydrodynamicvolume)-[:IS_A]->(emmo_hydrodynamicvolume)

MERGE(intensity:Property {name: "intensity"+row.PIDA,
                          flag: "findich",
                          date_added: "02/21/23"})
  ON CREATE
  SET intensity.uid = randomUUID()
MERGE(measurement)-[:HAS_MEASUREMENT_OUTPUT {value: apoc.convert.toList(toFloat(row.intensities))}]->(intensity)
MERGE(intensity)-[:IS_A]->(emmo_intensity)