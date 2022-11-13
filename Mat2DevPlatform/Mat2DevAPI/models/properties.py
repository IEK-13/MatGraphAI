from neomodel import (RelationshipTo, RelationshipFrom, StringProperty)
from django.db.models import ForeignKey, CASCADE
from Mat2DevAPI.models.abstractclasses import CausalObject
from django.db import models


class PhysicalDimension(CausalObject):
    class Meta:
        app_label = 'Mat2DevAPI'



class Property(PhysicalDimension):
    type = StringProperty(required=True, unique_index=True)
    derived_property = RelationshipTo(models.ForeignKey(
        "Property",
        on_delete=models.deletion.CASCADE), "derivedFrom")
    property = RelationshipFrom(models.ForeignKey(
        "Measurement",
        on_delete=models.deletion.CASCADE),
                                "YIELDS_PROP")


class VolumetricProperty(Property):
    pass


class MechanicalProperty(Property):
    pass


class OpticalProperty(Property):
    pass


class DeviceProperty(Property):
    pass


class ChemicalProperty(Property):
    pass


class Parameter(PhysicalDimension):
    parameter = RelationshipFrom(models.ForeignKey(
        "Process",
        on_delete=models.deletion.CASCADE),
        "usesParameter")
