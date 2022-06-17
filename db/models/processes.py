from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
                      FloatProperty, UniqueIdProperty, RelationshipTo)

from compositions import (Component, Material, Element)

config.DATABASE_URL = 'bolt://neo4j:herrklo1@localhost:11003/fuel-cells'  # default


class Process(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    element = RelationshipTo(Element, "PROCESSED")
    material = RelationshipTo(Material, "PROCESSED")
    component = RelationshipTo(Component, "PROCESSED")
