from neomodel import (IntegerProperty,
                      StringProperty,
                      DateTimeProperty,
                      ArrayProperty)
from neomodel import (RelationshipTo,
RelationshipFrom,
                      FloatProperty)

from Mat2DevAPI.choices.ChoiceFields import COMPONENT_TYPE_CHOICES, MATERIAL_STRUCTURE_CHOICEFIELD, \
    MATERIAL_MACROSTRUCTURE_CHOICEFIELD, MATERIAL_MICROSTRUCTURE_CHOICEFIELD, MATERIAL_NANOSTRUCTURE_CHOICEFIELD, \
    MATERIAL_LABEL_CHOICEFIELD
from Mat2DevAPI.models.abstractclasses import CausalObject, UIDDjangoNode
from django.db import models

from Mat2DevAPI.models.relationships import isManufacturingInputRel, hasManufacturingOutputRel, isMeasuredRel, \
    hasPartRel


class Matter(CausalObject):
    isManufactured = RelationshipTo(
        models.ForeignKey("Manufacturing",
                          on_delete=models.deletion.CASCADE), isManufacturingInputRel,
        model=isManufacturingInputRel)
    isOutput = RelationshipTo(
        models.ForeignKey("Manufacturing",
                          on_delete=models.deletion.CASCADE),
        isManufacturingInputRel,
        model=hasManufacturingOutputRel)
    measured = RelationshipTo(models.ForeignKey("Measurement",
                                                on_delete=models.deletion.CASCADE),
                              isMeasuredRel,
                              model=isMeasuredRel)


class ChemicalEntity(Matter):
    pass


class Element(ChemicalEntity):
    name = StringProperty(unique_index= True, required = True)
    abbreviation = StringProperty(required=True, unique_index= True)
    summary = StringProperty()




class Molecule(ChemicalEntity):
    class Meta(UIDDjangoNode.Meta):
        pass
    elements = RelationshipFrom('Mat2DevAPI.models.matter.Element', 'HAS_PART', model=hasPartRel)

    # IDENTIFIERS
    SMILES = StringProperty()
    InChI_key = StringProperty()
    InChI = StringProperty()
    CompoundCID = IntegerProperty()
    IUPAC_name = StringProperty()
    chemical_formula = StringProperty()
    CAS = StringProperty()

    # GENERAL PROPERTIES
    AlternativeNames = ArrayProperty()
    n_atoms = IntegerProperty()
    molar_weight = FloatProperty()
    charge = IntegerProperty()

    # ADDITIONAL INFORMATION

    # def __str__(self):
    #     return self.name

class Manufactured(Matter):
    hasElement = RelationshipTo(Element, hasPartRel, model=hasPartRel)
    hasMolecule = RelationshipTo(Molecule, hasPartRel, model=hasPartRel)
    pass


class Material(Manufactured):
    sumFormula = StringProperty()
    hasElement = RelationshipTo(Element, hasPartRel, model=hasPartRel)
    structure = ArrayProperty(StringProperty(choices = MATERIAL_STRUCTURE_CHOICEFIELD))
    nanostructure = ArrayProperty(StringProperty(choices = MATERIAL_NANOSTRUCTURE_CHOICEFIELD))
    microstructure = ArrayProperty(StringProperty(choices = MATERIAL_MICROSTRUCTURE_CHOICEFIELD))
    macrostructure = ArrayProperty(StringProperty(choices = MATERIAL_MACROSTRUCTURE_CHOICEFIELD))
    additional_label = ArrayProperty(StringProperty(choices = MATERIAL_LABEL_CHOICEFIELD))





class Component(Manufactured):
    type = StringProperty(choices=COMPONENT_TYPE_CHOICES, required=True)
    hasMaterial = RelationshipTo(Material, hasPartRel, model=hasPartRel)
    hasComponent = RelationshipTo(
        "Component", hasPartRel, model=hasPartRel)
    pass

class Device(Manufactured):
    hasMaterial = RelationshipTo(Material, hasPartRel, model=hasPartRel)
    hasComponent = RelationshipTo(
        Component, hasPartRel, model=hasPartRel)
    pass
