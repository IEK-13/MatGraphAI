from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
                      FloatProperty, UniqueIdProperty, RelationshipTo, ArrayProperty,
                      DateTimeProperty)


class NamedNode(StructuredNode):
    name = StringProperty(required=True)
    __abstract_node__ = True


class UniqueNamedNode(NamedNode):
    uid = UniqueIdProperty()
    __abstract_node__ = True


class UniqueNode(StructuredNode):
    name = UniqueIdProperty()
    __abstract_node__ = True


class PhysicalDescriptorNode(StructuredNode):
    type = StringProperty(required=True)
    scalarvalue = FloatProperty()
    valuevector = ArrayProperty()
    description = StringProperty()
    scalarerror = FloatProperty()
    errorvector = ArrayProperty()
    minVal = FloatProperty()
    maxVal = FloatProperty()
    __abstract_node__ = True


class Process(UniqueNamedNode):
    uid = UniqueIdProperty()
    year = DateTimeProperty()
    parameter = RelationshipTo("Parameter", "USED_PARAMETER")
    researcher = RelationshipTo("Researcher", "BY_RESEARCHER")
    instrument = RelationshipTo("Instrument", "USED_INSTRUMENT")
    __abstract_node__ = True


class Object(UniqueNode):
    name = StringProperty()
    type = StringProperty()
    process = RelationshipTo("FabricationProcess", "PROCESSED")
    process = RelationshipTo("Measurement", "MEASURED")
    __abstract_node__ = True
