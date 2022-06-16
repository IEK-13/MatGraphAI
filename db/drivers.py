from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
                        FloatProperty, UniqueIdProperty, RelationshipTo)

config.DATABASE_URL = 'bolt://neo4j:herrklo1@localhost:11003/fuel-cells'  # default


# tag::Component[]
class Component(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    cid = UniqueIdProperty()
# end::Component[]

# tag::Material[]
class Material(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    mid = UniqueIdProperty()
# end::Material[]

# tag::Element[]
class Element(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    eid = UniqueIdProperty()
# end::Element[]

# tag::Property[]
class Property(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    type = StringProperty(unique_index=True, required=True)
    value = FloatProperty()
    minVal = FloatProperty()
    maxVal = FloatProperty()
    error = FloatProperty()
# end::Property[]

# tag::Unit[]
class Unit(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
# end::Unit[]

# tag::Process[]
class Process(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
# end::Process[]

# tag::Instrument[]
class Process(StructuredNode):
    instrument = StringProperty(unique_index=True, required=True)
    model = StringProperty(unique_index=True, required=True)
# end::Process[]
