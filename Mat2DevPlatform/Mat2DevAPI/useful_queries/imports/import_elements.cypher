LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Mat2DevPlatform/Mat2DevAPI/data/materials/elements.csv' AS line

MATCH(atomicnumber:EMMO_Quantity {EMMO__name: "AtomicNumber"}),
     (atomicmass:EMMO_Quantity {EMMO__name: "AtomicMass"}),
     (molarheat:EMMO_Quantity {EMMO__name: "MolarHeat"}),
     (elementalsubstance:EMMO_Matter {EMMO__name: "ElementalSubstance"}),
     (density:EMMO_Quantity {EMMO__name: "Density"}),
     (melt:EMMO_Quantity {EMMO__name: "MeltingPoint"}),
     (electronegativity:EMMO_Quantity {EMMO__name: "ElectronegativityPauling"}),
     (electronaffinity:EMMO_Quantity {EMMO__name: "ElectronAffinity"}),
     (ionizationenergy:EMMO_Quantity {EMMO__name: "IonizationEnergy"})



// Create Nodes
CREATE (Matter:Matter:Element {name: line.name, summary: line.name, symbol : line.symbol})
MERGE (Matter)-[:IS_A]->(elementalsubstance)

FOREACH(x IN CASE WHEN line.discovered_by IS NOT NULL THEN [1] END |
  MERGE (researcher:Researcher {name: line.discovered_by})
    ON CREATE SET
    researcher.uid = randomUUID()
  CREATE (exp:Manufacturing {uid: randomUUID()})
  MERGE (Matter)<-[:IS_MANUFACTURING_OUTPUT]-(exp)-[:BY]->(researcher))
// IntegerProperties

CREATE (Matter)-[:HAS_PROPERTY {value : toInteger(line.number)}]->(atomicnumber)

//FloatProperties
FOREACH(x IN CASE WHEN NOT NULL in apoc.convert.toIntList(line.ionization_energies) THEN [1] END |
  MERGE(pionizationenergy:Property{uid: randomUUID(),
                          date_added : "1111-11-11"
  })
  MERGE (Matter)-[:HAS_PROPERTY {value: apoc.convert.toIntList(line.ionization_energies)}]
  ->(pionizationenergy)-[:IS_A]->(ionizationenergy))

FOREACH(x IN CASE WHEN line.electron_affinity IS NOT NULL THEN [1] END |
  MERGE(pelaff:Property{uid: randomUUID(),
                                   date_added : "1111-11-11"
  })
  MERGE (Matter)-[:HAS_PROPERTY {value: toFloat(line.electron_affinity)}]->(pelaff)-[:IS_A]->(electronaffinity))

FOREACH(x IN CASE WHEN line.electronegativity_pauling IS NOT NULL THEN [1] END |
  MERGE(pelneg:Property{uid: randomUUID(),
                                   date_added : "1111-11-11"
  })
  MERGE (Matter)-[:HAS_PROPERTY {value: toFloat(line.electronegativity_pauling)}]->(pelneg)-[:IS_A]->(electronegativity))

FOREACH(x IN CASE WHEN line.melt IS NOT NULL THEN [1] END |
  MERGE(pmelt:Property{uid: randomUUID(),
                                   date_added : "1111-11-11"
  })
  MERGE (Matter)-[:HAS_PROPERTY {value: toFloat(line.melt)}]->(pmelt)-[:IS_A]->(melt))

FOREACH(x IN CASE WHEN line.density IS NOT NULL THEN [1] END |
  MERGE(pdensity:Property{uid: randomUUID(),
                                   date_added : "1111-11-11"
  })
  MERGE (Matter)-[:HAS_PROPERTY {value: toFloat(line.density)}]->(pdensity)-[:IS_A]->(density))

FOREACH(x IN CASE WHEN line.molarheat IS NOT NULL THEN [1] END |
  MERGE(pmolarheat:Property{uid: randomUUID(),
                                   date_added : "1111-11-11"
  })
  MERGE (Matter)-[:HAS_PROPERTY {value: toFloat(line.number)}]->(pmolarheat)-[:IS_A]->(molarheat))

FOREACH(x IN CASE WHEN toFloat(line.atomic_mass) IS NOT NULL THEN [1] END |
  MERGE(patomicmass:Property{uid: randomUUID(),
                                   date_added : "1111-11-11"
  })
  MERGE (Matter)-[:HAS_PROPERTY {value: toFloat(line.atomic_mass)}]->(patomicmass)-[:IS_A]-(atomicmass));