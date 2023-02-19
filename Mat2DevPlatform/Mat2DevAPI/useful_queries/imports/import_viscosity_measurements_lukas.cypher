MATCH(researcher:Researcher {last_name: row.Researcher})
MATCH(material:Material {name:row.Material})
MERGE(measurement:Measurement {PIDA: row.PIDA,
date_added: "heute",
experiment_start: row.TestStart,
experiment_end: row.TestEnd,
instrument: row.Instrument})
MERGE(material)-[:IS_MEASUREMENT_INPUT]->(measurement)
