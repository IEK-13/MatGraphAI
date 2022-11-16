call n10s.graphconfig.init({
  baseSchemaPrefix:"EMMO",
  subClassOfRel:"IS_A"}
);

call n10s.nsprefixes.addFromText('

@prefix ifc: <http://standards.buildingsmart.org/IFC/DEV/IFC4_3/RC1/OWL#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix dce: <http://purl.org/dc/elements/1.1/> .
@prefix vann: <http://purl.org/vocab/vann/> .
@prefix list: <https://w3id.org/list#> .
@prefix expr: <https://w3id.org/express#> .
@prefix cc: <http://creativecommons.org/ns#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

') ;
// first pass, load the onto. Note that there are irregular uris, but we accept them with verifyUriSyntax: false 
call n10s.onto.import.fetch(
"https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/quantities.owl",
"Turtle", { verifyUriSyntax: false }) ;
call n10s.onto.import.fetch(
"https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/materials.owl",
"Turtle", { verifyUriSyntax: false }) ;
// we want named instances to link to the classes imported from the onto, so we change the handleRDFTypes mode.

call n10s.graphconfig.set({handleRDFTypes: "NODES",force:true}) ;

// second pass to load the owl:NamedIndividual 
call n10s.rdf.stream.fetch(
"https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/quantities.owl","Turtle", { verifyUriSyntax: false , limit :100000}) yield subject, predicate, object
where predicate = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type" and
object = "http://www.w3.org/2002/07/owl#EMMO_Quantity"
with collect(subject) as namedIndividuals
call n10s.rdf.stream.fetch(
"https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/quantities.owl","Turtle", { verifyUriSyntax: false , limit :100000}) yield subject, predicate, object, isLiteral, literalType, literalLang, subjectSPO
  where subject in namedIndividuals and not ( predicate = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type" and object = "http://www.w3.org/2002/07/owl#EMMO_Quantity" )
with n10s.rdf.collect(subject, predicate, object, isLiteral, literalType, literalLang, subjectSPO) as individualsAsRDF
call n10s.rdf.import.inline(individualsAsRDF, "N-Triples",{verifyUriSyntax: false}) yield terminationStatus,triplesLoaded, triplesParsed, namespaces, extraInfo, callParams
return terminationStatus,triplesLoaded, triplesParsed, namespaces, extraInfo, callParams ;

// add label to owl:NamedIndividual
match (ni:Resource)-[:EMMO__IS_A]->()
with distinct ni
set ni:EMMO_Quantity;

call n10s.rdf.stream.fetch(
"https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/materials.owl","Turtle", { verifyUriSyntax: false , limit :100000}) yield subject, predicate, object
where predicate = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type" and
object = "http://www.w3.org/2002/07/owl#Material"
with collect(subject) as namedIndividuals
call n10s.rdf.stream.fetch(
"https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/materials.owl","Turtle", { verifyUriSyntax: false , limit :100000}) yield subject, predicate, object, isLiteral, literalType, literalLang, subjectSPO
  where subject in namedIndividuals and not ( predicate = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type" and object = "http://www.w3.org/2002/07/owl#Material" )
with n10s.rdf.collect(subject, predicate, object, isLiteral, literalType, literalLang, subjectSPO) as individualsAsRDF
call n10s.rdf.import.inline(individualsAsRDF, "N-Triples",{verifyUriSyntax: false}) yield terminationStatus,triplesLoaded, triplesParsed, namespaces, extraInfo, callParams
return terminationStatus,triplesLoaded, triplesParsed, namespaces, extraInfo, callParams ;

// add label to owl:NamedIndividual
match (ni:Resource)-[:EMMO__IS_A]->()
with distinct ni
set ni:EMMO_Material;