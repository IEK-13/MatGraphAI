// Solvents import starts here

LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Mat2DevPlatform/Mat2DevAPI/data/materials/solvents1.csv' AS row

MATCH (avgmass:EMMO_Quantity {EMMO__name: "Mass"}),
      (monoisomass:EMMO_Quantity {EMMO__name: "MonoIsotopicMass"}),
      (c:Element {symbol: "C"}),
      (h:Element {symbol: "H"}),
      (o:Element {symbol: "O"}),
      (n:Element {symbol: "N"}),
      (f:Element {symbol: "F"}),
      (cl:Element {symbol: "Cl"}),
      (p:Element {symbol: "P"}),
      (br:Element {symbol: "Br"}),
      (i:Element {symbol: "I"}),
      (s:Element {symbol: "S"}),
      (v:Element {symbol: "V"}),
      (m:EMMO_Matter {EMMO__name: "Solvent"})


CREATE(solvent:Molecule{name: row.PREFERREDNAME,
                        SMILES: row.SMILES,
                        InChi_Key: row.INCHIKEY,
                        IUPAC_name: row.IUPACNAME,
                        InChi: row.INCHISTRING,
                        chemical_formula: row.MOLECULARFORMULA,
                        date_added: date(),
                        uid: randomUUID()})

MERGE (solvent)-[:IS_A]->(m)


FOREACH(x IN CASE WHEN row.C IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.C)}]->(c))

FOREACH(x IN CASE WHEN row.H IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.H)}]->(h))

FOREACH(x IN CASE WHEN row.O IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.O)}]->(o))

FOREACH(x IN CASE WHEN row.N IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.N)}]->(n))

FOREACH(x IN CASE WHEN row.F IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.F)}]->(f))

FOREACH(x IN CASE WHEN row.Cl IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.Cl)}]->(cl))

FOREACH(x IN CASE WHEN row.P IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.P)}]->(p))

FOREACH(x IN CASE WHEN row.Br IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.Br)}]->(br))

FOREACH(x IN CASE WHEN row.I IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.I)}]->(i))

FOREACH(x IN CASE WHEN row.S IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.S)}]->(s))

FOREACH(x IN CASE WHEN row.V IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.V)}]->(v))

FOREACH(x IN CASE WHEN row.AVERAGEMASS IS NOT NULL THEN [1] END |
  MERGE(pavgmass:Property{uid: randomUUID(),
                          date_added : date()
  })
  MERGE (solvent)-[:HAS_PROPERTY {value: toFloat(row.AVERAGEMASS)}]->(pavgmass)-[:IS_A]->(avgmass))

FOREACH(x IN CASE WHEN toFloat(row.MONOISOTOPICMASS) IS NOT NULL THEN [1] END |
  MERGE(pmonoisomass:Property{uid: randomUUID(),
                          date_added : date()
  })
  MERGE (solvent)-[:HAS_PROPERTY {value: toFloat(row.MONOISOTOPICMASS)}]->(pmonoisomass)-[:IS_A]-(monoisomass));


LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Mat2DevPlatform/Mat2DevAPI/data/materials/solvents2.csv' AS row

MATCH (avgmass:EMMO_Quantity {EMMO__name: "Mass"}),
      (monoisomass:EMMO_Quantity {EMMO__name: "MonoIsotopicMass"}),
      (c:Element {symbol: "C"}),
      (h:Element {symbol: "H"}),
      (o:Element {symbol: "O"}),
      (n:Element {symbol: "N"}),
      (f:Element {symbol: "F"}),
      (cl:Element {symbol: "Cl"}),
      (p:Element {symbol: "P"}),
      (br:Element {symbol: "Br"}),
      (i:Element {symbol: "I"}),
      (s:Element {symbol: "S"}),
      (v:Element {symbol: "V"}),
      (m:EMMO_Matter {EMMO__name: "Solvent"})


CREATE(solvent:Molecule{name: row.PREFERREDNAME,
                        SMILES: row.SMILES,
                        InChi_Key: row.INCHIKEY,
                        IUPAC_name: row.IUPACNAME,
                        InChi: row.INCHISTRING,
                        chemical_formula: row.MOLECULARFORMULA,
                        date_added: date(),
                        uid: randomUUID()})

MERGE (solvent)-[:IS_A]->(m)


FOREACH(x IN CASE WHEN row.C IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.C)}]->(c))

FOREACH(x IN CASE WHEN row.H IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.H)}]->(h))

FOREACH(x IN CASE WHEN row.O IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.O)}]->(o))

FOREACH(x IN CASE WHEN row.N IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.N)}]->(n))

FOREACH(x IN CASE WHEN row.F IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.F)}]->(f))

FOREACH(x IN CASE WHEN row.Cl IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.Cl)}]->(cl))

FOREACH(x IN CASE WHEN row.P IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.P)}]->(p))

FOREACH(x IN CASE WHEN row.Br IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.Br)}]->(br))

FOREACH(x IN CASE WHEN row.I IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.I)}]->(i))

FOREACH(x IN CASE WHEN row.S IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.S)}]->(s))

FOREACH(x IN CASE WHEN row.V IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.V)}]->(v))

FOREACH(x IN CASE WHEN row.AVERAGEMASS IS NOT NULL THEN [1] END |
  MERGE(pavgmass:Property{uid: randomUUID(),
                          date_added : date()
  })
  MERGE (solvent)-[:HAS_PROPERTY {value: toFloat(row.AVERAGEMASS)}]->(pavgmass)-[:IS_A]->(avgmass))

FOREACH(x IN CASE WHEN toFloat(row.MONOISOTOPICMASS) IS NOT NULL THEN [1] END |
  MERGE(pmonoisomass:Property{uid: randomUUID(),
                              date_added : date()
  })
  MERGE (solvent)-[:HAS_PROPERTY {value: toFloat(row.MONOISOTOPICMASS)}]->(pmonoisomass)-[:IS_A]-(monoisomass));

LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Mat2DevPlatform/Mat2DevAPI/data/materials/solvents3.csv' AS row

MATCH (avgmass:EMMO_Quantity {EMMO__name: "Mass"}),
      (monoisomass:EMMO_Quantity {EMMO__name: "MonoIsotopicMass"}),
      (c:Element {symbol: "C"}),
      (h:Element {symbol: "H"}),
      (o:Element {symbol: "O"}),
      (n:Element {symbol: "N"}),
      (f:Element {symbol: "F"}),
      (cl:Element {symbol: "Cl"}),
      (p:Element {symbol: "P"}),
      (br:Element {symbol: "Br"}),
      (i:Element {symbol: "I"}),
      (s:Element {symbol: "S"}),
      (v:Element {symbol: "V"}),
      (m:EMMO_Matter {EMMO__name: "Solvent"})


CREATE(solvent:Molecule{name: row.PREFERREDNAME,
                        SMILES: row.SMILES,
                        InChi_Key: row.INCHIKEY,
                        IUPAC_name: row.IUPACNAME,
                        InChi: row.INCHISTRING,
                        chemical_formula: row.MOLECULARFORMULA,
                        date_added: date(),
                        uid: randomUUID()})

MERGE (solvent)-[:IS_A]->(m)


FOREACH(x IN CASE WHEN row.C IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.C)}]->(c))

FOREACH(x IN CASE WHEN row.H IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.H)}]->(h))

FOREACH(x IN CASE WHEN row.O IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.O)}]->(o))

FOREACH(x IN CASE WHEN row.N IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.N)}]->(n))

FOREACH(x IN CASE WHEN row.F IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.F)}]->(f))

FOREACH(x IN CASE WHEN row.Cl IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.Cl)}]->(cl))

FOREACH(x IN CASE WHEN row.P IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.P)}]->(p))

FOREACH(x IN CASE WHEN row.Br IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.Br)}]->(br))

FOREACH(x IN CASE WHEN row.I IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.I)}]->(i))

FOREACH(x IN CASE WHEN row.S IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.S)}]->(s))

FOREACH(x IN CASE WHEN row.V IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.V)}]->(v))

FOREACH(x IN CASE WHEN row.AVERAGEMASS IS NOT NULL THEN [1] END |
  MERGE(pavgmass:Property{uid: randomUUID(),
                          date_added : date()
  })
  MERGE (solvent)-[:HAS_PROPERTY {value: toFloat(row.AVERAGEMASS)}]->(pavgmass)-[:IS_A]->(avgmass))

FOREACH(x IN CASE WHEN toFloat(row.MONOISOTOPICMASS) IS NOT NULL THEN [1] END |
  MERGE(pmonoisomass:Property{uid: randomUUID(),
                              date_added : date()
  })
  MERGE (solvent)-[:HAS_PROPERTY {value: toFloat(row.MONOISOTOPICMASS)}]->(pmonoisomass)-[:IS_A]-(monoisomass));

LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Mat2DevPlatform/Mat2DevAPI/data/materials/solvents4.csv' AS row

MATCH (avgmass:EMMO_Quantity {EMMO__name: "Mass"}),
      (monoisomass:EMMO_Quantity {EMMO__name: "MonoIsotopicMass"}),
      (c:Element {symbol: "C"}),
      (h:Element {symbol: "H"}),
      (o:Element {symbol: "O"}),
      (n:Element {symbol: "N"}),
      (f:Element {symbol: "F"}),
      (cl:Element {symbol: "Cl"}),
      (p:Element {symbol: "P"}),
      (br:Element {symbol: "Br"}),
      (i:Element {symbol: "I"}),
      (s:Element {symbol: "S"}),
      (v:Element {symbol: "V"}),
      (m:EMMO_Matter {EMMO__name: "Solvent"})


CREATE(solvent:Molecule{name: row.PREFERREDNAME,
                        SMILES: row.SMILES,
                        InChi_Key: row.INCHIKEY,
                        IUPAC_name: row.IUPACNAME,
                        InChi: row.INCHISTRING,
                        chemical_formula: row.MOLECULARFORMULA,
                        date_added: date(),
                        uid: randomUUID()})
MERGE (solvent)-[:IS_A]->(m)


FOREACH(x IN CASE WHEN row.C IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.C)}]->(c))

FOREACH(x IN CASE WHEN row.H IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.H)}]->(h))

FOREACH(x IN CASE WHEN row.O IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.O)}]->(o))

FOREACH(x IN CASE WHEN row.N IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.N)}]->(n))

FOREACH(x IN CASE WHEN row.F IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.F)}]->(f))

FOREACH(x IN CASE WHEN row.Cl IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.Cl)}]->(cl))

FOREACH(x IN CASE WHEN row.P IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.P)}]->(p))

FOREACH(x IN CASE WHEN row.Br IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.Br)}]->(br))

FOREACH(x IN CASE WHEN row.I IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.I)}]->(i))

FOREACH(x IN CASE WHEN row.S IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.S)}]->(s))

FOREACH(x IN CASE WHEN row.V IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.V)}]->(v))

FOREACH(x IN CASE WHEN row.AVERAGEMASS IS NOT NULL THEN [1] END |
  MERGE(pavgmass:Property{uid: randomUUID(),
                          date_added : date()
  })
  MERGE (solvent)-[:HAS_PROPERTY {value: toFloat(row.AVERAGEMASS)}]->(pavgmass)-[:IS_A]->(avgmass))

FOREACH(x IN CASE WHEN toFloat(row.MONOISOTOPICMASS) IS NOT NULL THEN [1] END |
  MERGE(pmonoisomass:Property{uid: randomUUID(),
                              date_added : date()
  })
  MERGE (solvent)-[:HAS_PROPERTY {value: toFloat(row.MONOISOTOPICMASS)}]->(pmonoisomass)-[:IS_A]-(monoisomass));

LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Mat2DevPlatform/Mat2DevAPI/data/materials/solvents5.csv' AS row

MATCH (avgmass:EMMO_Quantity {EMMO__name: "Mass"}),
      (monoisomass:EMMO_Quantity {EMMO__name: "MonoIsotopicMass"}),
      (c:Element {symbol: "C"}),
      (h:Element {symbol: "H"}),
      (o:Element {symbol: "O"}),
      (n:Element {symbol: "N"}),
      (f:Element {symbol: "F"}),
      (cl:Element {symbol: "Cl"}),
      (p:Element {symbol: "P"}),
      (br:Element {symbol: "Br"}),
      (i:Element {symbol: "I"}),
      (s:Element {symbol: "S"}),
      (v:Element {symbol: "V"}),
      (m:EMMO_Matter {EMMO__name: "Solvent"})


CREATE(solvent:Molecule{name: row.PREFERREDNAME,
                        SMILES: row.SMILES,
                        InChi_Key: row.INCHIKEY,
                        IUPAC_name: row.IUPACNAME,
                        InChi: row.INCHISTRING,
                        chemical_formula: row.MOLECULARFORMULA,
                        date_added: date(),
                        uid: randomUUID()})
MERGE (solvent)-[:IS_A]->(m)


FOREACH(x IN CASE WHEN row.C IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.C)}]->(c))

FOREACH(x IN CASE WHEN row.H IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.H)}]->(h))

FOREACH(x IN CASE WHEN row.O IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.O)}]->(o))

FOREACH(x IN CASE WHEN row.N IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.N)}]->(n))

FOREACH(x IN CASE WHEN row.F IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.F)}]->(f))

FOREACH(x IN CASE WHEN row.Cl IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.Cl)}]->(cl))

FOREACH(x IN CASE WHEN row.P IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.P)}]->(p))

FOREACH(x IN CASE WHEN row.Br IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.Br)}]->(br))

FOREACH(x IN CASE WHEN row.I IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.I)}]->(i))

FOREACH(x IN CASE WHEN row.S IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.S)}]->(s))

FOREACH(x IN CASE WHEN row.V IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.V)}]->(v))

FOREACH(x IN CASE WHEN row.AVERAGEMASS IS NOT NULL THEN [1] END |
  MERGE(pavgmass:Property{uid: randomUUID(),
                          date_added : date()
  })
  MERGE (solvent)-[:HAS_PROPERTY {value: toFloat(row.AVERAGEMASS)}]->(pavgmass)-[:IS_A]->(avgmass))

FOREACH(x IN CASE WHEN toFloat(row.MONOISOTOPICMASS) IS NOT NULL THEN [1] END |
  MERGE(pmonoisomass:Property{uid: randomUUID(),
                              date_added : date()
  })
  MERGE (solvent)-[:HAS_PROPERTY {value: toFloat(row.MONOISOTOPICMASS)}]->(pmonoisomass)-[:IS_A]-(monoisomass));

LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Mat2DevPlatform/Mat2DevAPI/data/materials/solvents6.csv' AS row

MATCH (avgmass:EMMO_Quantity {EMMO__name: "Mass"}),
      (monoisomass:EMMO_Quantity {EMMO__name: "MonoIsotopicMass"}),
      (c:Element {symbol: "C"}),
      (h:Element {symbol: "H"}),
      (o:Element {symbol: "O"}),
      (n:Element {symbol: "N"}),
      (f:Element {symbol: "F"}),
      (cl:Element {symbol: "Cl"}),
      (p:Element {symbol: "P"}),
      (br:Element {symbol: "Br"}),
      (i:Element {symbol: "I"}),
      (s:Element {symbol: "S"}),
      (v:Element {symbol: "V"}),
      (m:EMMO_Matter {EMMO__name: "Solvent"})


CREATE(solvent:Molecule{name: row.PREFERREDNAME,
    SMILES: row.SMILES,
    InChi_Key: row.INCHIKEY,
    IUPAC_name: row.IUPACNAME,
    InChi: row.INCHISTRING,
    chemical_formula: row.MOLECULARFORMULA,
    date_added: date(),
    uid: randomUUID()})

MERGE (solvent)-[:IS_A]->(m)


FOREACH(x IN CASE WHEN row.C IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.C)}]->(c))

FOREACH(x IN CASE WHEN row.H IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.H)}]->(h))

FOREACH(x IN CASE WHEN row.O IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.O)}]->(o))

FOREACH(x IN CASE WHEN row.N IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.N)}]->(n))

FOREACH(x IN CASE WHEN row.F IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.F)}]->(f))

FOREACH(x IN CASE WHEN row.Cl IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.Cl)}]->(cl))

FOREACH(x IN CASE WHEN row.P IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.P)}]->(p))

FOREACH(x IN CASE WHEN row.Br IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.Br)}]->(br))

FOREACH(x IN CASE WHEN row.I IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.I)}]->(i))

FOREACH(x IN CASE WHEN row.S IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.S)}]->(s))

FOREACH(x IN CASE WHEN row.V IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: toInteger(row.V)}]->(v))

FOREACH(x IN CASE WHEN row.AVERAGEMASS IS NOT NULL THEN [1] END |
  MERGE(pavgmass:Property{uid: randomUUID(),
                          date_added : date()
  })
  MERGE (solvent)-[:HAS_PROPERTY {value: toFloat(row.AVERAGEMASS)}]->(pavgmass)-[:IS_A]->(avgmass))

FOREACH(x IN CASE WHEN toFloat(row.MONOISOTOPICMASS) IS NOT NULL THEN [1] END |
  MERGE(pmonoisomass:Property{uid: randomUUID(),
                              date_added : date()
  })
  MERGE (solvent)-[:HAS_PROPERTY {value: toFloat(row.MONOISOTOPICMASS)}]->(pmonoisomass)-[:IS_A]-(monoisomass));


