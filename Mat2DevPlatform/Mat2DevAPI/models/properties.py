from neomodel import (RelationshipTo, RelationshipFrom, StringProperty)
from django.db.models import ForeignKey, CASCADE
from Mat2DevAPI.models.abstractclasses import CausalObject
from django.db import models
from Mat2DevAPI.models.abstractclasses import UIDDjangoNode, OntologyNode



class PhysicalDimension(CausalObject):
    class Meta:
        app_label = 'Mat2DevAPI'
    __abstract_node__ = True




class Property(PhysicalDimension):
    class Meta:
        verbose_name_plural = 'properties'
        app_label = 'Mat2DevAPI'
    type = StringProperty(required=True, unique_index=True)
    derived_property = RelationshipTo(models.ForeignKey(
        "Property",
        on_delete=models.deletion.CASCADE), "derivedFrom")
    property = RelationshipFrom(models.ForeignKey(
        "Measurement",
        on_delete=models.deletion.CASCADE),
                                "YIELDS_PROP")


class Parameter(PhysicalDimension):
    parameter = RelationshipFrom(models.ForeignKey(
        "Process",
        on_delete=models.deletion.CASCADE),
        "usesParameter")
