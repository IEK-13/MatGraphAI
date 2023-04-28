//Import of ontologies, first neosemantic gets initialized, subsequently the ontologies can be imported, each domain gets
//an additional label to "EMMO_DOMAIN" to make the different domains separately accessible

Match (n)-[m]-(r) delete n,m,r;
Match (n) delete n;

//CREATE CONSTRAINT n10s_unique_uri FOR (r:Resource) REQUIRE r.uri IS UNIQUE;

call n10s.graphconfig.init({
baseSchemaPrefix:"EMMO",
subClassOfRel:"IS_A"}
);

// first pass, load the onto. Note that there are irregular uris, but we accept them with verifyUriSyntax: false
call n10s.rdf.import.fetch("https://raw.githubusercontent.com/IEK-13/MatGraphAI/AddCSVAPI/Ontology/materials.owl","RDF/XML", { verifyUriSyntax: false }) ;
//call n10s.onto.import.fetch("https://raw.githubusercontent.com/IEK-13/MatGraphAI/AddCSVAPI/Ontology/quantities.owl","RDF/XML", { verifyUriSyntax: false }) ;
//call n10s.rdf.import.fetch("https://raw.githubusercontent.com/IEK-13/MatGraphAI/AddCSVAPI/Ontology/manufactured.owl","RDF/XML", { verifyUriSyntax: false }) ;
//call n10s.rdf.import.fetch("https://raw.githubusercontent.com/IEK-13/MatGraphAI/AddCSVAPI/Ontology/manufacturing.owl","RDF/XML", { verifyUriSyntax: false }) ;
//call n10s.onto.import.fetch("https://raw.githubusercontent.com/IEK-13/MatGraphAI/AddCSVAPI/Ontology/units.owl","Turtle", { verifyUriSyntax: false}) ;


// we want named instances to link to the classes imported from the onto, so we change the handleRDFTypes mode.
call n10s.graphconfig.set({handleRDFTypes: "NODES",force:true}) ;

// second pass to load the owl:Matter
call n10s.rdf.stream.fetch("https://raw.githubusercontent.com/IEK-13/MatGraphAI/AddCSVAPI/Ontology/manufactured.owl","RDF/XML",{ verifyUriSyntax: false , limit :100000}) yield subject, predicate, object
MATCH (n:Resource{uri:subject})
SET n:EMMO_Matter;

// second pass to load the owl:Matter
call n10s.rdf.stream.fetch("https://raw.githubusercontent.com/IEK-13/MatGraphAI/AddCSVAPI/Ontology/manufacturing.owl","RDF/XML", { verifyUriSyntax: false , limit :100000}) yield subject, predicate, object
MATCH (n:Resource{uri:subject})
SET n:EMMO_Process;

call n10s.rdf.stream.fetch("https://raw.githubusercontent.com/IEK-13/MatGraphAI/AddCSVAPI/Ontology/materials.owl","RDF/XML", { verifyUriSyntax: false , limit :100000}) yield subject, predicate, object
MATCH (n:Resource{uri:subject})
SET n:EMMO_Matter;

call n10s.rdf.stream.fetch("https://raw.githubusercontent.com/IEK-13/MatGraphAI/AddCSVAPI/Ontology/quantities.owl","RDF/XML", { verifyUriSyntax: false , limit :100000}) yield subject, predicate, object
MATCH (n:Resource{uri:subject})
SET n:EMMO_Quantity;

//call n10s.rdf.stream.fetch("https://raw.githubusercontent.com/IEK-13/MatGraphAI/AddCSVAPI/Ontology/units.owl","RDF/XML", { verifyUriSyntax: false , limit :100000}) yield subject, predicate, object
//MATCH (n:Resource{uri:subject})
//WITH n.EMMO__label as label, n.EMMO__name as name, n
//SET n.EMMO__label = name
//SET n.EMMO__name = label
//SET n:EMMO_Unit;

MATCH(n)
WHERE n:EMMO__Relationship OR n:owl__AnnotationProperty OR n:owl__AllDisjointClasses
DETACH DELETE n;

MATCH (n)
WHERE n:Resource OR n:EMMO__Class OR n:owl__Class OR n:owl__Ontology
REMOVE n:Resource, n:EMMO__Class, n:owl__Class, n:owl__Ontology;


MATCH (n)
WHERE (n:EMMO_Matter OR n:EMMO_Process OR n:EMMO_Quantity OR n:EMMO_Unit) AND (n.uid) IS NOT NULL
SET n.uid = randomUUID()