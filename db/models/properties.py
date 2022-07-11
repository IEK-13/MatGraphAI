from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
                      FloatProperty, UniqueIdProperty, RelationshipTo, RelationshipFrom)

from abstractclasses import *


class Property(PhysicalDescriptorNode):
    property = RelationshipTo("Property", "DERIVED_FROM")
    property = RelationshipFrom("Measurement", "YIELDS_PROP")
    __abstract_node__ = True


class Measurement(Process):
    year = DateTimeProperty()
    pass


class OpticalProperty(Property):
    pass


class ElectricalProperty(Property):
    pass


class ChemicalProperty(Property):
    pass


class VolumetricProperty(Property):
    pass


class MechanicalProperty(Property):
    pass
