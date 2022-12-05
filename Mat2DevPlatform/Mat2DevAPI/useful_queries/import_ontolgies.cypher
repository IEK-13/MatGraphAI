//Import of ontologies, first neosemantic gets initialized, subsequently the ontologies can be imported, each domain gets
//an additional label to "EMMO_DOMAIN" to make the different domains separately accessible

//Match (n)-[m]-(r) delete n,m,r;
//Match (n) delete n;

// CREATE CONSTRAINT n10s_unique_uri ON (r:Resource) ASSERT r.uri IS UNIQUE;

//call n10s.graphconfig.init({
//baseSchemaPrefix:"EMMO",
//subClassOfRel:"IS_A"}
//);

// first pass, load the onto. Note that there are irregular uris, but we accept them with verifyUriSyntax: false
call n10s.onto.import.fetch("https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Ontology/materials.owl","Turtle", { verifyUriSyntax: false }) ;
call n10s.onto.import.fetch("https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Ontology/quantities.owl","Turtle", { verifyUriSyntax: false }) ;
call n10s.onto.import.fetch("https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Ontology/manufactured.owl","Turtle", { verifyUriSyntax: false }) ;
call n10s.onto.import.fetch("https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Ontology/manufacturing.owl","Turtle", { verifyUriSyntax: false }) ;

// we want named instances to link to the classes imported from the onto, so we change the handleRDFTypes mode.
call n10s.graphconfig.set({handleRDFTypes: "NODES",force:true}) ;

// second pass to load the owl:Material
call n10s.rdf.stream.fetch("https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Ontology/manufactured.owl","Turtle", { verifyUriSyntax: false , limit :100000}) yield subject, predicate, object
MATCH (n:Resource{uri:subject})
SET n:EMMO_Manufactured;

// second pass to load the owl:Material
call n10s.rdf.stream.fetch("https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Ontology/manufacturing.owl","Turtle", { verifyUriSyntax: false , limit :100000}) yield subject, predicate, object
MATCH (n:Resource{uri:subject})
SET n:EMMO_Manufacturing;

call n10s.rdf.stream.fetch("https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Ontology/materials.owl","Turtle", { verifyUriSyntax: false , limit :100000}) yield subject, predicate, object
MATCH (n:Resource{uri:subject})
SET n:EMMO_Material;

call n10s.rdf.stream.fetch("https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Ontology/quantities.owl","Turtle", { verifyUriSyntax: false , limit :100000}) yield subject, predicate, object
MATCH (n:Resource{uri:subject})
SET n:EMMO_Quantity;


