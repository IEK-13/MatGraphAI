



MATCH (emmo_cs:EMMO_Matter{EMMO__name:"AcetyleneBlack"})<-[:IS_A]-(m:Matter)<-[:HAS_PART]-(material:Matter),
      (device:Matter)-[:IS_A]->(emmo_fc:EMMO_Matter{EMMO__name:"FuelCell"}),
      p = (material)-[:IS_MANUFACTURING_INPUT| IS_MANUFACTURING_OUTPUT*]->(device)
WITH [node in nodes(p) WHERE (node:Matter)] as manufactured_list
UNWIND manufactured_list as manufactured
WITH DISTINCT manufactured ORDER BY manufactured.name
CALL{
    WITH manufactured
    MATCH (manufactured)-[:IS_A]->(manufactured_label:EMMO_Matter)
    WITH  manufactured,
          manufactured_label
    MATCH (manufactured)-[property:HAS_PROPERTY]->(property_node)-[:IS_A]->(property_label)
    WITH property_node, property_label, property
    CALL{
        WITH property_node
        MATCH (property_node)<-[:YIELDS_PROPERTY]-(:Measurement)-[parameter:HAS_PARAMETER]->(:Parameter)-[:IS_A]-(parameter_label:EMMO_Quantity)
        RETURN apoc.coll.toSet(collect(apoc.map.merge(apoc.map.fromValues(["name", parameter_label.EMMO__name]), parameter{.*}))) as parameter_map
    }
    RETURN apoc.coll.toSet(collect(apoc.map.merge(apoc.map.merge(apoc.map.fromValues(["name", property_label.EMMO__name]), property{.*}),
                                                                apoc.map.fromValues(["parameters", parameter_map])))) as property_list
}
MATCH (manufactured)-[:IS_A]->(manufactured_label:EMMO_Matter)
WITH DISTINCT manufactured,
              manufactured_label,
              property_list
OPTIONAL MATCH p1 = ((manufactured_label)-[:EMMO__IS_A*]->(:EMMO_Matter))
UNWIND nodes(p1) as alt_nodes
WITH manufactured,
     manufactured_label,
     property_list,
     apoc.coll.toSet(collect(alt_nodes.EMMO__name)) as alternative_label
WITH apoc.map.merge(apoc.map.fromValues(["label", manufactured_label.EMMO__name,"alternative_label", alternative_label]), manufactured{.*})
     as manufactured_map, manufactured, property_list
RETURN apoc.coll.toSet(collect(apoc.map.setKey(manufactured_map, "Properties", property_list)))