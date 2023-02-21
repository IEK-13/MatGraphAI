WITH ['IrO2-15wt-ic013-1Prop086_1.csv',
      'IrO2-15wt-ic013-1Prop086_2.csv',
      'IrO2-15wt-ic013-1Prop086_3.csv',
      'IrO2-35wt-ic02-1Prop86_1.csv',
      'IrO2-35wt-ic02-1Prop86_2.csv',
      'IrO2-35wt-ic02-1Prop86_3.csv',
      'IrO2-35wt-ic013-1Prop04_1.csv',
      'IrO2-35wt-ic013-1Prop04_2.csv',
      'IrO2-35wt-ic013-1Prop04_3.csv',
      'IrO2-35wt-ic013-1Prop086_1.csv',
      'TanakaPtC-IC065-1Prop088_1.csv',
      'TanakaPtC-IC065-1Prop088_2.csv',
      'TanakaPtC-IC065-1Prop088_3.csv',
      'UmicorePtC-IC065-1Prop088_1.csv',
      'UmicorePtC-IC065-1Prop088_2.csv'
      ] as filelist

LOAD CSV WITH HEADERS FROM
'https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Mat2DevPlatform/Mat2DevAPI/data/lukas/viscosity/UmicorePtC-IC065-1Prop088_2.csv'
AS row
CALL{
LOAD CSV WITH HEADERS FROM
'https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Mat2DevPlatform/Mat2DevAPI/data/lukas/viscosity/UmicorePtC-IC065-1Prop088_2.csv'
AS row1
RETURN collect(TOFLOAT(row1.Speed)) AS speedlist,
collect(TOFLOAT(row1.Time)) AS timelist,
collect(TOFLOAT(row1.Torque)) AS torquelist,
collect(TOFLOAT(row1.Viscosity)) AS viscositylist,
collect(TOFLOAT(row1.`Shear Stress`)) AS shearstresslist,
collect(TOFLOAT(row1.`Shear Rate`)) AS shearratelist,
collect(TOFLOAT(row1.`Accuracy`)) AS accuracylist
}


MATCH(researcher:Researcher {last_name:row.Researcher})
MATCH(material:Material {name:row.Material})
MATCH(emmo_measurement:EMMO_Process {EMMO__name:row.Ontology})
MATCH(emmo_viscosity:EMMO_Quantity {EMMO__name:"Viscosity"})
MATCH(emmo_torque:EMMO_Quantity {EMMO__name:"Torque"})
MATCH(emmo_speed:EMMO_Quantity {EMMO__name:"Speed"})
MATCH(emmo_shearstress:EMMO_Quantity {EMMO__name:"ShearStress"})
MATCH(emmo_shearrate:EMMO_Quantity {EMMO__name:"ShearRate"})
MATCH(emmo_time:EMMO_Quantity {EMMO__name:"Time"})



MERGE(measurement:Measurement {PIDA:row.PIDA,
date_added:date(),
experiment_start:row.TestStart,
experiment_end:row.TestEnd,
instrument:row.Instrument})
ON CREATE
SET measurement.uid = randomUUID()
MERGE(material)- [:IS_MEASUREMENT_INPUT] - >(measurement)
MERGE(measurement)- [:BY] - >(researcher)

MERGE(speed:Parameter {name:"Speed_" + row.PIDA,
date_added:date(),
flag:"findich"
})
ON CREATE
SET speed.uid = randomUUID()
MERGE(measurement)- [:HAS_PARAMETER {value:speedlist}]- >(speed)
MERGE(speed)- [:IS_A] - >(emmo_speed)

MERGE(torque:Parameter {name:"Torque_" + row.PIDA,
date_added:date(),
flag:"findich"
})
ON CREATE
SET torque.uid = randomUUID()
MERGE(measurement)- [:HAS_PARAMETER {value:torquelist}]- >(torque)
MERGE(torque)- [:IS_A] - >(emmo_torque)

MERGE(time:Parameter {name:"Time_" + row.PIDA,
date_added:date(),
flag:"findich"
})
ON CREATE
SET time.uid = randomUUID()
MERGE(measurement)- [:HAS_PARAMETER {value:timelist}]- >(time)
MERGE(time)- [:IS_A] - >(emmo_time)

MERGE(viscosity:Property {name:"Viscosity_" + row.PIDA,
date_added:date(),
flag:"findich"
})
ON CREATE
SET viscosity.uid = randomUUID()
MERGE(measurement)- [:HAS_MEASUREMENT_OUTPUT {value:viscositylist, accuracy:accuracylist}] - >(viscosity)
MERGE(viscosity)- [:IS_A] - >(emmo_viscosity)


MERGE(shearrate:Property {name:"ShearRate_" + row.PIDA,
date_added:date(),
flag:"findich"
})
ON CREATE
SET shearrate.uid = randomUUID()
MERGE(measurement)- [:HAS_MEASUREMENT_OUTPUT {value:shearratelist}]- >(shearrate)
MERGE(shearrate)- [:IS_A] - >(emmo_shearrate)

MERGE(shearstress:Property {name:"ShearStress_" + row.PIDA,
date_added:date(),
flag:"findich"
})
ON CREATE
SET shearrate.uid = randomUUID()
MERGE(measurement)- [:HAS_MEASUREMENT_OUTPUT {value:shearstresslist}]- >(shearstress)
MERGE(emmo_shearstress)- [:IS_A] - >(emmo_shearstress)

