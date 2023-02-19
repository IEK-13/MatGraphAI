LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Mat2DevPlatform/Mat2DevAPI/data/lukas/viscosity/IrO2-15wt-ic013-1Prop086_1.csv' AS row
MATCH(researcher:Researcher {last_name: row.Researcher})
MATCH(material:Material {name:row.Material})
MATCH(emmo_measurement:EMMO_Process {EMMO__name: row.})
MERGE(measurement:Measurement {PIDA: row.PIDA,
date_added: "heute",
experiment_start: row.TestStart,
experiment_end: row.TestEnd,
instrument: row.Instrument})
MERGE(material)-[:IS_MEASUREMENT_INPUT]->(measurement)
MERGE(measurement)-[:BY]->(researcher)