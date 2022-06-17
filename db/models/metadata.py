from properties import Property
from processes import Process
from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
                      FloatProperty, UniqueIdProperty, RelationshipTo)

config.DATABASE_URL = 'bolt://neo4j:herrklo1@localhost:11003/fuel-cells'  # default
print("hi")


class Unit(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    property = RelationshipTo(Property, "HAS_DIM")


class Instrument(StructuredNode):
    instrument = StringProperty(unique_index=True, required=True)
    model = StringProperty(unique_index=True, required=True)
    process = RelationshipTo(Process, "PROCESSED_WITH")


class Researcher(StructuredNode):
    instrument = StringProperty(unique_index=True, required=True)
    model = StringProperty(unique_index=True, required=True)
    process = RelationshipTo(Process, "PROCESSED_BY")
