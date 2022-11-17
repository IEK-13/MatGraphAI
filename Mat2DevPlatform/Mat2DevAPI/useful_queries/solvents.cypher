Match (n)-[m]-(r) delete n,m,r;
Match (n) delete n;

call n10s.graphconfig.init({
  baseSchemaPrefix:"EMMO",
  subClassOfRel:"IS_A"}
);

// first pass, load the onto. Note that there are irregular uris, but we accept them with verifyUriSyntax: false
call n10s.onto.import.fetch("https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/materials.owl","Turtle", { verifyUriSyntax: false }) ;
call n10s.onto.import.fetch("https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/quantities.owl","Turtle", { verifyUriSyntax: false }) ;

// we want named instances to link to the classes imported from the onto, so we change the handleRDFTypes mode.
call n10s.graphconfig.set({handleRDFTypes: "NODES",force:true}) ;

// second pass to load the owl:Material
call n10s.rdf.stream.fetch("https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/materials.owl","Turtle", { verifyUriSyntax: false , limit :100000}) yield subject, predicate, object
MATCH (n:Resource{uri:subject})
SET n:EMMO_Material;

call n10s.rdf.stream.fetch("https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/quantities.owl","Turtle", { verifyUriSyntax: false , limit :100000}) yield subject, predicate, object
MATCH (n:Resource{uri:subject})
SET n:EMMO_Quantity;


LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Mat2DevPlatform/Mat2DevAPI/data/elements.csv' AS line

MATCH(atomicnumber:EMMO_Quantity {EMMO__name: "AtomicNumber"}),
     (atomicmass:EMMO_Quantity {EMMO__name: "AtomicMass"}),
     (molarheat:EMMO_Quantity {EMMO__name: "MolarHeat"}),
     (density:EMMO_Quantity {EMMO__name: "Density"}),
     (melt:EMMO_Quantity {EMMO__name: "MeltingPoint"}),
     (electronegativity:EMMO_Quantity {EMMO__name: "ElectronegativityPauling"}),
     (electronaffinity:EMMO_Quantity {EMMO__name: "ElectronAffinity"}),
     (ionizationenergy:EMMO_Quantity {EMMO__name: "IonizationEnergy"})



// Create Nodes
CREATE (element:Element {name: line.name, summary: line.summary, symbol : line.symbol})


FOREACH(x IN CASE WHEN line.discovered_by IS NOT NULL THEN [1] END |
  MERGE (researcher:Researcher {name: line.discovered_by})
    ON CREATE SET
    researcher.uid = randomUUID()
  CREATE (exp:Manufacturing {uid: randomUUID()})
  MERGE (element)<-[:YIELDED]-(exp)-[:BY]->(researcher))
// IntegerProperties

CREATE (element)-[:HAS_INTEGER_PROPERTY {value : line.number}]->(atomicnumber)

//FloatProperties

CREATE (element)-[:HAS_FLOAT_PROPERTY {value : toFloat(line.atomic_mass)}]->(atomicmass)
CREATE (element)-[:HAS_FLOAT_PROPERTY {value : toFloat(line.number)}]->(molarheat)
CREATE (element)-[:HAS_FLOAT_PROPERTY {value : toFloat(line.density)}]->(density)
CREATE (element)-[:HAS_FLOAT_PROPERTY {value : toFloat(line.melt)}]->(melt)
CREATE (element)-[:HAS_FLOAT_PROPERTY {value : toFloat(line.electronegativity_pauling)}]->(electronegativity)
CREATE (element)-[:HAS_FLOAT_PROPERTY {value : toFloat(line.electron_affinity)}]->(electronaffinity)
CREATE (element)-[:HAS_FLOAT_PROPERTY {value : toFloat(line.ionization_energies)}]->(ionizationenergy);

// Solvents import starts here

LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Mat2DevPlatform/Mat2DevAPI/data/solvents1.csv' AS row

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
      (v:Element {symbol: "V"})


CREATE(solvent:Molecule {name: row.PREFERREDNAME,
SMILES : row.SMILES,
InChi_Key : row.INCHIKEY,
IUPAC_name : row.IUPACNAME,
InChi: row.INCHISTRING,
chemical_formula: row.MOLECULARFORMULA})


FOREACH(x IN CASE WHEN row.C IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.C}]->(c))

FOREACH(x IN CASE WHEN row.H IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.H}]->(h))

FOREACH(x IN CASE WHEN row.O IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.O}]->(o))

FOREACH(x IN CASE WHEN row.N IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.N}]->(n))

FOREACH(x IN CASE WHEN row.F IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.F}]->(f))

FOREACH(x IN CASE WHEN row.Cl IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.Cl}]->(cl))

FOREACH(x IN CASE WHEN row.P IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.P}]->(p))

FOREACH(x IN CASE WHEN row.Br IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.Br}]->(br))

FOREACH(x IN CASE WHEN row.I IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.I}]->(i))

FOREACH(x IN CASE WHEN row.S IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.S}]->(s))

FOREACH(x IN CASE WHEN row.V IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.V}]->(v));

LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Mat2DevPlatform/Mat2DevAPI/data/solvents2.csv' AS row

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
      (v:Element {symbol: "V"})


CREATE(solvent:Molecule {name: row.PREFERREDNAME,
                         SMILES : row.SMILES,
                         InChi_Key : row.INCHIKEY,
                         IUPAC_name : row.IUPACNAME,
                         InChi: row.INCHISTRING,
                         chemical_formula: row.MOLECULARFORMULA})


FOREACH(x IN CASE WHEN row.C IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.C}]->(c))

FOREACH(x IN CASE WHEN row.H IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.H}]->(h))

FOREACH(x IN CASE WHEN row.O IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.O}]->(o))

FOREACH(x IN CASE WHEN row.N IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.N}]->(n))

FOREACH(x IN CASE WHEN row.F IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.F}]->(f))

FOREACH(x IN CASE WHEN row.Cl IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.Cl}]->(cl))

FOREACH(x IN CASE WHEN row.P IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.P}]->(p))

FOREACH(x IN CASE WHEN row.Br IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.Br}]->(br))

FOREACH(x IN CASE WHEN row.I IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.I}]->(i))

FOREACH(x IN CASE WHEN row.S IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.S}]->(s))

FOREACH(x IN CASE WHEN row.V IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.V}]->(v));

LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Mat2DevPlatform/Mat2DevAPI/data/solvents3.csv' AS row

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
      (v:Element {symbol: "V"})


CREATE(solvent:Molecule {name: row.PREFERREDNAME,
                         SMILES : row.SMILES,
                         InChi_Key : row.INCHIKEY,
                         IUPAC_name : row.IUPACNAME,
                         InChi: row.INCHISTRING,
                         chemical_formula: row.MOLECULARFORMULA})


FOREACH(x IN CASE WHEN row.C IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.C}]->(c))

FOREACH(x IN CASE WHEN row.H IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.H}]->(h))

FOREACH(x IN CASE WHEN row.O IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.O}]->(o))

FOREACH(x IN CASE WHEN row.N IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.N}]->(n))

FOREACH(x IN CASE WHEN row.F IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.F}]->(f))

FOREACH(x IN CASE WHEN row.Cl IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.Cl}]->(cl))

FOREACH(x IN CASE WHEN row.P IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.P}]->(p))

FOREACH(x IN CASE WHEN row.Br IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.Br}]->(br))

FOREACH(x IN CASE WHEN row.I IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.I}]->(i))

FOREACH(x IN CASE WHEN row.S IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.S}]->(s))

FOREACH(x IN CASE WHEN row.V IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.V}]->(v));

LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Mat2DevPlatform/Mat2DevAPI/data/solvents4.csv' AS row

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
      (v:Element {symbol: "V"})


CREATE(solvent:Molecule {name: row.PREFERREDNAME,
                         SMILES : row.SMILES,
                         InChi_Key : row.INCHIKEY,
                         IUPAC_name : row.IUPACNAME,
                         InChi: row.INCHISTRING,
                         chemical_formula: row.MOLECULARFORMULA})


FOREACH(x IN CASE WHEN row.C IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.C}]->(c))

FOREACH(x IN CASE WHEN row.H IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.H}]->(h))

FOREACH(x IN CASE WHEN row.O IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.O}]->(o))

FOREACH(x IN CASE WHEN row.N IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.N}]->(n))

FOREACH(x IN CASE WHEN row.F IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.F}]->(f))

FOREACH(x IN CASE WHEN row.Cl IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.Cl}]->(cl))

FOREACH(x IN CASE WHEN row.P IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.P}]->(p))

FOREACH(x IN CASE WHEN row.Br IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.Br}]->(br))

FOREACH(x IN CASE WHEN row.I IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.I}]->(i))

FOREACH(x IN CASE WHEN row.S IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.S}]->(s))

FOREACH(x IN CASE WHEN row.V IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.V}]->(v));

LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Mat2DevPlatform/Mat2DevAPI/data/solvents5.csv' AS row

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
      (v:Element {symbol: "V"})


CREATE(solvent:Molecule {name: row.PREFERREDNAME,
                         SMILES : row.SMILES,
                         InChi_Key : row.INCHIKEY,
                         IUPAC_name : row.IUPACNAME,
                         InChi: row.INCHISTRING,
                         chemical_formula: row.MOLECULARFORMULA})


FOREACH(x IN CASE WHEN row.C IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.C}]->(c))

FOREACH(x IN CASE WHEN row.H IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.H}]->(h))

FOREACH(x IN CASE WHEN row.O IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.O}]->(o))

FOREACH(x IN CASE WHEN row.N IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.N}]->(n))

FOREACH(x IN CASE WHEN row.F IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.F}]->(f))

FOREACH(x IN CASE WHEN row.Cl IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.Cl}]->(cl))

FOREACH(x IN CASE WHEN row.P IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.P}]->(p))

FOREACH(x IN CASE WHEN row.Br IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.Br}]->(br))

FOREACH(x IN CASE WHEN row.I IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.I}]->(i))

FOREACH(x IN CASE WHEN row.S IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.S}]->(s))

FOREACH(x IN CASE WHEN row.V IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.V}]->(v));

LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Mat2DevPlatform/Mat2DevAPI/data/solvents6.csv' AS row

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
      (v:Element {symbol: "V"})


CREATE(solvent:Molecule {name: row.PREFERREDNAME,
                         SMILES : row.SMILES,
                         InChi_Key : row.INCHIKEY,
                         IUPAC_name : row.IUPACNAME,
                         InChi: row.INCHISTRING,
                         chemical_formula: row.MOLECULARFORMULA})


FOREACH(x IN CASE WHEN row.C IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.C}]->(c))

FOREACH(x IN CASE WHEN row.H IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.H}]->(h))

FOREACH(x IN CASE WHEN row.O IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.O}]->(o))

FOREACH(x IN CASE WHEN row.N IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.N}]->(n))

FOREACH(x IN CASE WHEN row.F IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.F}]->(f))

FOREACH(x IN CASE WHEN row.Cl IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.Cl}]->(cl))

FOREACH(x IN CASE WHEN row.P IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.P}]->(p))

FOREACH(x IN CASE WHEN row.Br IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.Br}]->(br))

FOREACH(x IN CASE WHEN row.I IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.I}]->(i))

FOREACH(x IN CASE WHEN row.S IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.S}]->(s))

FOREACH(x IN CASE WHEN row.V IS NOT NULL THEN [1] END |
  MERGE (solvent)-[:HAS_PART {value: row.V}]->(v))



