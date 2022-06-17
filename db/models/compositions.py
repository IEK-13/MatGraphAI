from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
                      FloatProperty, UniqueIdProperty, RelationshipTo)

config.DATABASE_URL = 'bolt://neo4j:herrklo1@localhost:11003/fuel-cells'  # default


class Element(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    eid = UniqueIdProperty()


class Material(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    mid = UniqueIdProperty()
    component = RelationshipTo(Element, 'CONSISTS_OF')


class Component(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    cid = UniqueIdProperty()
    type = StringProperty(unique_index=True, required=True)
    component = RelationshipTo(Material, 'CONSISTS_OF')
