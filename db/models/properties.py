from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
                      FloatProperty, UniqueIdProperty, RelationshipTo, RelationshipFrom)

from abstractclasses import *
from dataproperties import *


class PhysicalDimension(CausalObject):
    pass


class Property(PhysicalDimension):
    derivedproperty = RelationshipTo("Property", "derivedFrom")
    property = RelationshipFrom("Measurement", "YIELDS_PROP")


class Parameter(PhysicalDimension):
    parameter = RelationshipFrom("Process", "usesParameter")


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
