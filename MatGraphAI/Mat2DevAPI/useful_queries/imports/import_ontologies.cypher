//Import of ontologies, first neosemantic gets initialized, subsequently the ontologies can be imported, each domain gets
//an additional label to "EMMO_DOMAIN" to make the different domains separately accessible

Match (n)-[m]-(r) delete n,m,r;
Match (n) delete n;
CREATE CONSTRAINT UniqueAlternativeLabel IF NOT EXISTS ON (al:alternative_Label) ASSERT al.name IS UNIQUE;

//CREATE CONSTRAINT n10s_unique_uri FOR (r:Resource) REQUIRE r.uri IS UNIQUE;

call n10s.graphconfig.init({
baseSchemaPrefix:"EMMO",
subClassOfRel:"IS_A"}
);
call n10s.graphconfig.set({handleRDFTypes: "NODES",force:true}) ;
//CALL n10s.graphconfig.init({ handleVocabUris: "MAP", handleMultival: "ARRAY" });
//CALL n10s.mapping.add("onto", "https://raw.githubusercontent.com/IEK-13/MatGraphAI/AddCSVAPI/Ontology/");
//CALL n10s.mapping.add("owl", "http://www.w3.org/2002/07/owl#");
//CALL n10s.mapping.add("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#");
//CALL n10s.mapping.add("rdfs", "http://www.w3.org/2000/01/rdf-schema#");
//CALL n10s.mapping.add("xsd", "http://www.w3.org/2001/XMLSchema#");
// first pass, load the onto. Note that there are irregular uris, but we accept them with verifyUriSyntax: false
call n10s.onto.import.fetch("https://raw.githubusercontent.com/IEK-13/MatGraphAI/AddCSVAPI/Ontology/materials.owl","RDF/XML", { verifyUriSyntax: false }) ;
CALL n10s.rdf.stream.fetch("https://raw.githubusercontent.com/IEK-13/MatGraphAI/AddCSVAPI/Ontology/materials.owl", "RDF/XML", { verifyUriSyntax: false }) YIELD subject, predicate, object
WHERE predicate CONTAINS "alternative_label"
MATCH (cls:EMMO__Class { uri: subject })
MERGE (cls)<-[:IS_ALTERNATIVE_LABEL]-(al:Alternative_Label {name: object});


//CALL n10s.onto.import.fetch("https://raw.githubusercontent.com/IEK-13/MatGraphAI/AddCSVAPI/Ontology/quantities.owl","RDF/XML", { verifyUriSyntax: false }) ;
//CALL n10s.rdf.stream.fetch("https://raw.githubusercontent.com/IEK-13/MatGraphAI/AddCSVAPI/Ontology/quantities.owl", "RDF/XML") YIELD subject, predicate, object
//WHERE predicate CONTAINS "alternative_label"
//MATCH (cls:EMMO__Class { uri: subject })
//MERGE (cls)<-[:IS_ALTERNATIVE_LABEL]-(al:Alternative_Label {name: object});
//
//call n10s.onto.import.fetch("https://raw.githubusercontent.com/IEK-13/MatGraphAI/AddCSVAPI/Ontology/manufactured.owl","RDF/XML", { verifyUriSyntax: false }) ;
//CALL n10s.rdf.stream.fetch("https://raw.githubusercontent.com/IEK-13/MatGraphAI/AddCSVAPI/Ontology/manufactured.owl", "RDF/XML") YIELD subject, predicate, object
//WHERE predicate CONTAINS "alternative_label"
//MATCH (cls:EMMO__Class { uri: subject })
//MERGE (cls)<-[:IS_ALTERNATIVE_LABEL]-(al:Alternative_Label {name: object});
//
//call n10s.onto.import.fetch("https://raw.githubusercontent.com/IEK-13/MatGraphAI/AddCSVAPI/Ontology/manufacturing.owl","RDF/XML", { verifyUriSyntax: false }) ;
//CALL n10s.rdf.stream.fetch("https://raw.githubusercontent.com/IEK-13/MatGraphAI/AddCSVAPI/Ontology/manufacturing.owl", "RDF/XML") YIELD subject, predicate, object
//WHERE predicate CONTAINS "alternative_label"
//MATCH (cls:EMMO__Class { uri: subject })
//MERGE (cls)<-[:IS_ALTERNATIVE_LABEL]-(al:Alternative_Label {name: object});

//call n10s.onto.import.fetch("https://raw.githubusercontent.com/IEK-13/MatGraphAI/AddCSVAPI/Ontology/units.owl","RDF/XML", { verifyUriSyntax: false}) ;
//CALL n10s.rdf.stream.fetch("https://raw.githubusercontent.com/IEK-13/MatGraphAI/AddCSVAPI/Ontology/units.owl", "RDF/XML") YIELD subject, predicate, object
//WHERE predicate CONTAINS "alternative_label"
//MATCH (cls:EMMO__Class { uri: subject })
//MERGE (cls)<-[:IS_ALTERNATIVE_LABEL]-(al:Alternative_Label {name: object});


// we want named instances to link to the classes imported from the onto, so we change the handleRDFTypes mode.

// second pass to load the owl:Matter
//call n10s.rdf.stream.fetch("https://raw.githubusercontent.com/IEK-13/MatGraphAI/AddCSVAPI/Ontology/materials.owl","RDF/XML",{ verifyUriSyntax: false , limit :100000}) yield subject, predicate, object
//MATCH (n:Resource{uri:subject})
//SET n:EMMO_Matter;
//MATCH (cls:EMMO__Class)
//WHERE EXISTS(cls.alternative_label)
//UNWIND cls.alternative_label AS alt_label
//MERGE (al:Alternative_Label {name: alt_label})
//CREATE (cls)-[:HAS_ALTERNATIVE_LABEL]->(al);
////second pass to load the owl:Matter
//call n10s.rdf.stream.fetch("https://raw.githubusercontent.com/IEK-13/MatGraphAI/AddCSVAPI/Ontology/manufacturing.owl","RDF/XML", { verifyUriSyntax: false , limit :100000}) yield subject, predicate, object
//MATCH (n:Resource{uri:subject})
//SET n:EMMO_Process;



// second pass to load the owl:Matter
//call n10s.rdf.stream.fetch("https://raw.githubusercontent.com/IEK-13/MatGraphAI/AddCSVAPI/Ontology/manufacturing.owl","RDF/XML", { verifyUriSyntax: false , limit :100000}) yield subject, predicate, object
//MATCH (n:Resource{uri:subject})
//SET n:EMMO_Process;
//
//call n10s.rdf.stream.fetch("https://raw.githubusercontent.com/IEK-13/MatGraphAI/AddCSVAPI/Ontology/materials.owl","RDF/XML", { verifyUriSyntax: false , limit :100000}) yield subject, predicate, object
//MATCH (n:Resource{uri:subject})
//SET n:EMMO_Matter;
//
//call n10s.rdf.stream.fetch("https://raw.githubusercontent.com/IEK-13/MatGraphAI/AddCSVAPI/Ontology/quantities.owl","RDF/XML", { verifyUriSyntax: false , limit :100000}) yield subject, predicate, object
//MATCH (n:Resource{uri:subject})
//SET n:EMMO_Quantity;

//call n10s.rdf.stream.fetch("https://raw.githubusercontent.com/IEK-13/MatGraphAI/AddCSVAPI/Ontology/units.owl","RDF/XML", { verifyUriSyntax: false , limit :100000}) yield subject, predicate, object
//MATCH (n:Resource{uri:subject})
//WITH n.EMMO__label as label, n.EMMO__name as name, n
//SET n.EMMO__label = name
//SET n.EMMO__name = label
//SET n:EMMO_Unit;

//MATCH(n)
//WHERE n:EMMO__Relationship OR n:owl__AnnotationProperty OR n:owl__AllDisjointClasses
//DETACH DELETE n;
//
//MATCH (n)
//WHERE n:Resource OR n:EMMO__Class OR n:owl__Class OR n:owl__Ontology
//REMOVE n:Resource, n:EMMO__Class, n:owl__Class, n:owl__Ontology;


//MATCH (n)
//WHERE (n:EMMO_Matter OR n:EMMO_Process OR n:EMMO_Quantity OR n:EMMO_Unit) AND (n.uid) IS NOT NULL
//SET n.uid = randomUUID()