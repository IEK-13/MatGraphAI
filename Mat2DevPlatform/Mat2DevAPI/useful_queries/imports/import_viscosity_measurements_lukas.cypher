LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Mat2DevPlatform/Mat2DevAPI/data/lukas/viscosity/IrO2-15wt-ic013-1Prop086_1.csv' AS row
WITH row, collect(row.Speed) as speedlist
MATCH(researcher:Researcher {last_name: row.Researcher})
MATCH(material:Material {name:row.Material})
MATCH(emmo_measurement:EMMO_Process {EMMO__name: row.Ontology})
MATCH(emmo_viscosity:EMMO_Process {EMMO__name: "Viscosity"})
MATCH(emmo_torque:EMMO_Process {EMMO__name: "Torque"})
MATCH(emmo_speed:EMMO_Process {EMMO__name: "Speed"})
MATCH(emmo_shearstress:EMMO_Process {EMMO__name: "ShearStress"})
MATCH(emmo_shearrate:EMMO_Process {EMMO__name: "ShearRate"})


MERGE(measurement:Measurement {PIDA: row.PIDA,
date_added: "heute",
experiment_start: row.TestStart,
experiment_end: row.TestEnd,
instrument: row.Instrument})
  ON CREATE
  SET measurement.uid = randomUUID()
MERGE(material)-[:IS_MEASUREMENT_INPUT]->(measurement)
MERGE(measurement)-[:BY]->(researcher)

MERGE(speed:Parameter {name: "Speed",
date_added: "heute"})
  ON CREATE
  SET speed.uid = randomUUID()
MERGE(measurement)-[:HAS_PARAMETER {value: speedlist}]->(speed)
MERGE(time:Parameter {name: "Time",
                       date_added: "heute"})
  ON CREATE
  SET time.uid = randomUUID()
MERGE(viscosity:Property {name: "Viscosity",
                      date_added: "heute"})
  ON CREATE
  SET viscosity.uid = randomUUID()