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

LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Mat2DevPlatform/Mat2DevAPI/useful_queries/elements.csv' AS line

MATCH(atomicnumber:EMMO_Quantity {EMMO__name: "AtomicNumber"}), (atomicmass:EMMO_Quantity {EMMO__name: "AtomicMass"}), (molarheat:EMMO_Quantity {EMMO__name: "MolarHeat"}), (density:EMMO_Quantity {EMMO__name: "Density"})
return atomicmass, molarheat, density
// Create Nodes
//CREATE (element:Element {name: line.name, summary: line.summary, abbreviation : line.symbol})
//
//
//FOREACH(x IN CASE WHEN line.discovered_by IS NOT NULL THEN [1] END |
//  MERGE (researcher:Researcher {name: line.discovered_by})
//  ON CREATE SET
//    researcher.uid = randomUUID()
//  CREATE (exp:Manufacturing {uid: randomUUID()})
//  MERGE (element)<-[:YIELDED]-(exp)-[:BY]->(researcher))
//// IntegerProperties
//
//CREATE (element)-[:HAS_INTEGER_PROPERTY {value : line.number}]->(atomicnumber)
//
////FloatProperties
//
//CREATE (element)-[:HAS_FLOAT_PROPERTY {value : toFloat(line.atomic_mass)}]->(atomicmass)
//CREATE (element)-[:HAS_FLOAT_PROPERTY {value : toFloat(line.number)}]->(molarheat)
//CREATE (element)-[:HAS_FLOAT_PROPERTY {value : toFloat(line.density)}]->(density)
//

// 