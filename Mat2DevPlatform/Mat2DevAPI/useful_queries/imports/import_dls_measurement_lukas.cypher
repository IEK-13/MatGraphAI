LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Mat2DevPlatform/Mat2DevAPI/data/lukas/viscosity/IrO2-15wt-ic013-1Prop086_1.csv' AS row

MATCH(researcher:Researcher {first_name: row.Researcher})
MATCH(material:Material {name:row.Material})
MATCH(emmo_measurement:EMMO_Process {EMMO__name: row.Ontology})

MATCH(emmo_hydrodynamicdiameter:EMMO_Quantity {EMMO__name: "HydrodynamicDiameter"})
MATCH(emmo_averagehydrodynamicdiameter:EMMO_Quantity {EMMO__name: "AverageHydrodynamicDiameter"})
MATCH(emmo_hydrodynamicvolume:EMMO_Quantity {EMMO__name: "HydrodynamicVolume"})
MATCH(emmo_intensity:EMMO_Quantity {EMMO__name: "Intensity"})
MATCH(emmo_pdi:EMMO_Quantity {EMMO__name: "PolyDispersityIndex"})



MERGE(measurement:Measurement {PIDA: row.PIDA,
                               date_added: "heute",
                               experiment_start: row.`Measurement Data and Time`,
                               experiment_end: row.`Measurement Data and Time`,
                               instrument: row.Instrument})
  ON CREATE
  SET measurement.uid = randomUUID()

MERGE(material)-[:IS_MEASUREMENT_INPUT]->(measurement)
MERGE(measurement)-[:BY]->(researcher)

MERGE(hydrodynamicdiameter:Property {name: "hydrodynamicdiameter"+row.PIDA,
                       date_added: "02/21/23"})
  ON CREATE
  SET speed.uid = randomUUID()
MERGE(measurement)-[:HAS_MEASUREMENT_OUTPUT {value: apoc.convert.toFloatList(row.sizes)}]->(hydrodynamicdiameter)
MERGE(hydrodynamicdiameter)-[:IS_A]->(emmo_hydrodynamicdiameter)

MERGE(averagehydrodynamicdiameter:Property {name: "averagehydrodynamicdiameter"+row.PIDA,
                                     date_added: "02/21/23"})
  ON CREATE
  SET speed.uid = randomUUID()
MERGE(measurement)-[:HAS_MEASUREMENT_OUTPUT {value: toFloat(row.`Z-Average (d.nm)`)}]->(averagehydrodynamicdiameter)
MERGE(averagehydrodynamicdiameter)-[:IS_A]->(emmo_averagehydrodynamicdiameter)

MERGE(hydrodynamicvolume:Property {name: "hydrodynamicvolume"+row.PIDA,
                                            date_added: "02/21/23"})
  ON CREATE
  SET speed.uid = randomUUID()
MERGE(measurement)-[:HAS_MEASUREMENT_OUTPUT {value: apoc.convert.toFloatList(row.volumes)}]->(hydrodynamicvolume)
MERGE(hydrodynamicvolume)-[:IS_A]->(emmo_hydrodynamicvolume)

MERGE(intensity:Property {name: "intensity"+row.PIDA,
                                   date_added: "02/21/23"})
  ON CREATE
  SET speed.uid = randomUUID()
MERGE(measurement)-[:HAS_MEASUREMENT_OUTPUT {value: apoc.convert.toFloatList(row.intensities)}]->(intensity)
MERGE(intensity)-[:IS_A]->(emmo_intensity)



