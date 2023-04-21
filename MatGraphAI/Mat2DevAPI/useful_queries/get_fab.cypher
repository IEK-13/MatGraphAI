call apoc.meta.subGraph({ labels: ['EMMO_Matter', 'EMMO_Quantity', 'EMMO_Process', 'Matter', 'Property', 'Parameter', 'Measurement', 'Manufacturing'] })

//Get_Tables
Profile
MATCH (emmo_cs:EMMO_Matter{EMMO__name:"AcetyleneBlack"})<-[:IS_A]-(m:Matter)<-[:HAS_PART]-(material:Matter),
      (device:Matter)-[:IS_A]->(emmo_fc:EMMO_Matter{EMMO__name:"FuelCell"}),
      p = (material)-[:IS_MANUFACTURING_INPUT| IS_MANUFACTURING_OUTPUT*]->(device)


UNWIND (nodes(p)) as nodes
WITH (nodes:Matter) as ink, (nodes:Manufacturing) as manufacturing

RETURN manufacturing

MATCH (ink)-[property:HAS_PROPERTY]->(propertynode)-[:IS_A]->(label)
WITH collect(apoc.map.merge(apoc.map.fromValues(["name", label.EMMO__name]), property{.*})) as property_list, ink

MATCH (property)-[]-(measurement:Measurement)-[parameter:HAS_PARAMETER]
WITH apoc.map.fromValues(["Properties", property_list]) as property_map , ink, property_list
WITH ink{.*} as ink_map, ink, property_map, property_list

RETURN collect(apoc.map.setKey(ink_map, "Properties", property_list)), ink_map
  ORDER BY ink.name





Profile
MATCH (emmo_cs:EMMO_Matter{EMMO__name:"AcetyleneBlack"})<-[:IS_A]-(m:Matter)<-[:HAS_PART]-(material:Matter),
      (device:Matter)-[:IS_A]->(emmo_fc:EMMO_Matter{EMMO__name:"FuelCell"}),
      p = (material)-[:IS_MANUFACTURING_INPUT| IS_MANUFACTURING_OUTPUT*]->(device)

WITH [node in nodes(p) WHERE (node:Matter)] as manufactured_list,
     [node in nodes(p) WHERE (node:Manufacturing)] as manufacturing_list


UNWIND manufactured_list as manufactured
RETURN manufactured
ORDER BY manufactured.name
UNWIND manufacturing_list as manufacturing

MATCH (manufactured)-[:IS_A]->(manufactured_label:EMMO_Matter)
WITH DISTINCT manufactured,
     manufactured_label,
     manufacturing


MATCH (manufacturing)-[:IS_A]->(manufacturing_label:EMMO_Process)
WITH DISTINCT manufactured,
     manufactured_label,
     manufacturing,
     manufacturing_label


MATCH (manufactured)-[property:HAS_PROPERTY]->(property_node)-[:IS_A]->(property_label)
WITH DISTINCT manufactured,
     property,
     property_node,
     property_label,
     manufactured_label,
     manufacturing,
     manufacturing_label

MATCH (property_node)<-[:HAS_MEASUREMENT_OUTPUT]-(:Measurement)-[parameter:HAS_PARAMETER]->(:Parameter)-[:IS_A]-(parameter_label:EMMO_Quantity)
WITH  collect(apoc.map.merge(apoc.map.fromValues(["name", parameter_label.EMMO__name]), parameter{.*})) as parameter_map,
manufactured,
property,
property_node,
property_label,
manufactured_label,
manufacturing,
manufacturing_label

WITH collect(apoc.map.merge(apoc.map.merge(apoc.map.fromValues(["name", property_label.EMMO__name]), property{.*}), apoc.map.fromValues(["parameters", parameter_map]))) as property_list, manufactured, property_node
WITH apoc.map.fromValues(["Properties", property_list]) as property_map , manufactured, property_list
WITH manufactured{.*} as manufactured_map, manufactured, property_map, property_list

RETURN collect(apoc.map.setKey(manufactured_map, "Properties", property_list)), manufactured_map




// NEW


Profile
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
  MATCH (property_node)<-[:HAS_MEASUREMENT_OUTPUT]-(:Measurement)-[parameter:HAS_PARAMETER]->(:Parameter)-[:IS_A]-(parameter_label:EMMO_Quantity)
  RETURN  apoc.coll.toSet(collect(apoc.map.merge(apoc.map.fromValues(["name", parameter_label.EMMO__name]), parameter{.*}))) as parameter_map
  }
  RETURN apoc.coll.toSet(collect(apoc.map.merge(apoc.map.merge(apoc.map.fromValues(["name", property_label.EMMO__name]), property{.*}), apoc.map.fromValues(["parameters", parameter_map])))) as property_list

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

WITH apoc.map.merge(apoc.map.fromValues(["label", manufactured_label.EMMO__name,"alternative_label", alternative_label]), manufactured{.*}) as manufactured_map, manufactured, property_list
RETURN apoc.coll.toSet(collect(apoc.map.setKey(manufactured_map, "Properties", property_list)))
