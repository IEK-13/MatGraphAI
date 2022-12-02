//Import of ontologies, first neosemantic gets initialized, subsequently the ontologies can be imported, each domain gets
//an additional label to "EMMO_DOMAIN" to make the different domains separately accessible

Match (n)-[m]-(r) delete n,m,r;
Match (n) delete n;

// CREATE CONSTRAINT n10s_unique_uri ON (r:Resource) ASSERT r.uri IS UNIQUE;



call n10s.onto.import.fetch("materials.owl","Turtle", { verifyUriSyntax: false }) ;
call n10s.onto.import.fetch("quantities.owl","Turtle", { verifyUriSyntax: false }) ;



call n10s.rdf.stream.fetch("materials.owl","Turtle") yield subject
MATCH (n:Resource{uri:subject})
SET n:EMMO_Manufactured;



call n10s.rdf.stream.fetch("quantities.owl","Turtle") yield subject
MATCH (n:Resource{uri:subject})
SET n:EMMO_Quantity;