from django.db import models
from neomodel import (IntegerProperty,
                      StringProperty,
                      ArrayProperty)
from neomodel import (RelationshipTo,
                      RelationshipFrom)

from Mat2DevAPI.choices.ChoiceFields import MATERIAL_STRUCTURE_CHOICEFIELD, \
    MATERIAL_MACROSTRUCTURE_CHOICEFIELD, MATERIAL_MICROSTRUCTURE_CHOICEFIELD, MATERIAL_NANOSTRUCTURE_CHOICEFIELD
from Mat2DevAPI.models.abstractclasses import CausalObject, UIDDjangoNode
from Mat2DevAPI.models.relationships import isManufacturingInputRel, hasManufacturingOutputRel, isMeasuredRel, \
    hasPartRel


class Matter(CausalObject):
    isManufactured = RelationshipTo(models.ForeignKey("Manufacturing", on_delete=models.deletion.CASCADE),
        isManufacturingInputRel,
        model=isManufacturingInputRel)
    isOutput = RelationshipTo(models.ForeignKey("Manufacturing", on_delete=models.deletion.CASCADE),
        isManufacturingInputRel,
        model=hasManufacturingOutputRel)
    measured = RelationshipTo(models.ForeignKey("Measurement",
        on_delete=models.deletion.CASCADE),
        isMeasuredRel,
        model=isMeasuredRel)
    __abstract_node__ = True


class Manufactured(Matter):
    hasElement = RelationshipTo("Element", hasPartRel, model=hasPartRel)
    hasMolecule = RelationshipTo("Molecule", hasPartRel, model=hasPartRel)
    __abstract_node__ = True
    pass


class Element(Matter):
    name = StringProperty(unique_index=True, required=True)
    summary = StringProperty()
    symbol = StringProperty(required=True, unique_index=True)


class Molecule(Manufactured):
    class Meta(UIDDjangoNode.Meta):
        pass
    elements = RelationshipFrom('Mat2DevAPI.models.matter.Element', 'HAS_PART', model=hasPartRel)
    # IDENTIFIERS
    SMILES = StringProperty()
    InChI_key = StringProperty()
    InChI = StringProperty()
    compound_cid = IntegerProperty()
    IUPAC_name = StringProperty()
    chemical_formula = StringProperty()
    CAS = StringProperty()
    alternative_names = ArrayProperty()


# GENERAL PROPERTIES

# ADDITIONAL INFORMATION

# def __str__(self):
#     return self.name


class Material(Manufactured):
    sumFormula = StringProperty()
    hasElement = RelationshipTo(Element, hasPartRel, model=hasPartRel)
    structure = ArrayProperty(StringProperty(choices=MATERIAL_STRUCTURE_CHOICEFIELD))
    nanostructure = ArrayProperty(StringProperty(choices=MATERIAL_NANOSTRUCTURE_CHOICEFIELD))
    microstructure = ArrayProperty(StringProperty(choices=MATERIAL_MICROSTRUCTURE_CHOICEFIELD))
    macrostructure = ArrayProperty(StringProperty(choices=MATERIAL_MACROSTRUCTURE_CHOICEFIELD))


class Component(Manufactured):
    hasMaterial = RelationshipTo(Material, hasPartRel, model=hasPartRel)
    hasComponent = RelationshipTo("Component", hasPartRel, model=hasPartRel)
    pass


class Device(Manufactured):
    hasMaterial = RelationshipTo(Material, hasPartRel, model=hasPartRel)
    hasComponent = RelationshipTo(Component, hasPartRel, model=hasPartRel)
    pass
