from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
                      FloatProperty, UniqueIdProperty, RelationshipTo, RelationshipFrom)

from abstractclasses import *


class PhysicalDimension(Physical):
    pass


class Property(PhysicalDimension):
    derivedproperty = RelationshipTo("Property", "derivedFrom")
    property = RelationshipFrom("Measurement", "YIELDS_PROP")


class Parameter(PhysicalDimension):
    parameter = RelationshipFrom("Process", "usesParameter")


class Property(PhysicalDimension):
    property = RelationshipTo("Property", "DERIVED_FROM")
    property = RelationshipFrom("Measurement", "YIELDS_PROP")
    __abstract_node__ = True


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
