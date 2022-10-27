from neomodel import (RelationshipTo, RelationshipFrom)

from Mat2DevAPI.models.abstractclasses import *


class PhysicalDimension(CausalObject):
    class Meta:
        app_label = 'Mat2DevAPI'
    pass


class Property(PhysicalDimension):
    derivedproperty = RelationshipTo("Property", "derivedFrom")
    property = RelationshipFrom("Measurement", "YIELDS_PROP")


class Parameter(PhysicalDimension):
    parameter = RelationshipFrom("Process", "usesParameter")
