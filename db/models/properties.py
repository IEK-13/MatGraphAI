from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
                      FloatProperty, UniqueIdProperty, RelationshipTo)

config.DATABASE_URL = 'bolt://neo4j:herrklo1@localhost:11003/fuel-cells'  # default


class Property(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    type = StringProperty(unique_index=True, required=True)
    value = FloatProperty()
    minVal = FloatProperty()
    maxVal = FloatProperty()
    error = FloatProperty()
    property = RelationshipTo("Property", "DERIVED_FROM")


class Parameter(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    value = FloatProperty()
    error = FloatProperty()
    property = RelationshipTo("Property", "DERIVED_FROM")
