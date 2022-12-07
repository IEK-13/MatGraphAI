//Import of ontologies, first neosemantic gets initialized, subsequently the ontologies can be imported, each domain gets
//an additional label to "EMMO_DOMAIN" to make the different domains separately accessible

Match (n)-[m]-(r) delete n,m,r;
Match (n) delete n;
