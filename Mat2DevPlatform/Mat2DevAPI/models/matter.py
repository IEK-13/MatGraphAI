from django.db.models import ForeignKey, CASCADE
from neomodel import IntegerProperty, RelationshipFrom
from neomodel import (RelationshipTo, FloatProperty)

from Mat2DevAPI.choices.ChoiceFields import COMPONENT_TYPE_CHOICES
from Mat2DevAPI.models import hasPart, isManufacturingInput, hasManufacturingOutput, \
    isMeasured
from Mat2DevAPI.models.abstractclasses import *


class Matter(CausalObject):
    isManufactured = RelationshipTo(
        ForeignKey("Manufacturing", on_delete=CASCADE, verbose_name='Manufacturing Details'), "isMeasurementInput",
        model=isManufacturingInput)
    isOutput = RelationshipFrom(ForeignKey("Manufacturing", on_delete=CASCADE, verbose_name='Manufacturing Details'),
                                "isManufacturingOutput",
                                model=hasManufacturingOutput)
    measured = RelationshipTo(ForeignKey("Measurement", on_delete=CASCADE, verbose_name='Manufacturing Details'),
                              "isMeasured",
                              model=isMeasured)


class ChemicalEntity(Matter):
    pass


class Molecule(ChemicalEntity):
    # IDENTIFIERS
    SMILES = StringProperty()
    InChIKey = StringProperty()
    InChI = StringProperty()
    CompoundCID = IntegerProperty()
    IUPACName = StringProperty()
    sumFormula = StringProperty()
    CAS = StringProperty()

    # GENERAL PROPERTIES
    AlternativeNames = ArrayProperty()
    nAtoms = IntegerProperty()
    molWeight = FloatProperty()
    charge = IntegerProperty()

    # ADDITIONAL INFORMATION
    date_added = DateTimeProperty()
    hasAtom = RelationshipTo("Element", "hasPart", model=hasPart)


class Element(ChemicalEntity):
    pass


class Manufactured(Matter):
    hasElement = RelationshipTo("Element", "hasPart", model=hasPart)
    hasMolecule = RelationshipTo("Molecule", "hasPart", model=hasPart)
    pass


class Material(Manufactured):
    pass


class Component(Manufactured):

    type = StringProperty(choices=COMPONENT_TYPE_CHOICES, required=True)
    hasMaterial = RelationshipTo("Material", "hasPart", model=hasPart)
    hasComponent = RelationshipTo(
        "Component", "hasPart", model=hasPart)


class Device(Manufactured):
    hasMaterial = RelationshipTo("Material", "hasPart", model=hasPart)
    hasComponent = RelationshipTo(
        "Component", "hasPart", model=hasPart)
    pass
