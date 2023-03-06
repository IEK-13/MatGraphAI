from neomodel import (IntegerProperty, StringProperty, ZeroOrMore)
from neomodel import (RelationshipTo,
                      RelationshipFrom)

from Mat2DevAPI.models.abstractclasses import CausalObject, UIDDjangoNode
from Mat2DevAPI.models.relationships import isManufacturingInputRel, hasPartRel, isARel, isManufacturingOutputRel, \
    hasMeasurementOutputRel, hasProcessOutputRel


class Matter(CausalObject):
    properties = RelationshipTo('Mat2DevAPI.models.properties.Property', 'HAS_PROPERTY', model=hasProcessOutputRel)
    is_a = RelationshipTo('Mat2DevAPI.models.ontology.EMMO_Matter', 'IS_A', cardinality = ZeroOrMore, model=isARel)
    manufacturing_input = RelationshipTo('Mat2DevAPI.models.processes.Manufacturing', 'IS_MANUFACTURING_INPUT', model=isManufacturingInputRel)
    manufacturing_output = RelationshipFrom('Mat2DevAPI.models.processes.Manufacturing', 'IS_MANUFACTURING_OUTPUT', model=isManufacturingOutputRel)
    measurement_input = RelationshipTo('Mat2DevAPI.models.processes.Measurement', 'IS_MEASUREMENT_INPUT', model=hasMeasurementOutputRel)
    __abstract_node__ = True


class Manufactured(Matter):
    elements = RelationshipTo('Mat2DevAPI.models.matter.Element', "HAS_PART", model=hasPartRel)
    molecules = RelationshipTo('Mat2DevAPI.models.matter.Molecule', "HAS_PART", model=hasPartRel)
    __abstract_node__ = True
    pass


class Element(Matter):
    name = StringProperty(unique_index=True, required=True)
    summary = StringProperty()
    symbol = StringProperty(required=True, unique_index=True)


class Molecule(Manufactured):
    class Meta(UIDDjangoNode.Meta):
        pass
    # IDENTIFIERS
    SMILES = StringProperty()
    InChI_key = StringProperty()
    InChI = StringProperty()
    compound_cid = IntegerProperty()
    IUPAC_name = StringProperty()
    chemical_formula = StringProperty()
    CAS = StringProperty()



class Material(Manufactured):

    sumFormula = StringProperty()
    materials = RelationshipTo('Mat2DevAPI.models.matter.Material', "HAS_PART", model=hasPartRel)




class Component(Manufactured):
    materials = RelationshipTo('Mat2DevAPI.models.matter.Material', "HAS_PART", model=hasPartRel)
    components = RelationshipTo('Mat2DevAPI.models.matter.Component', 'HAS_PART', model=hasPartRel)
    pass


class Device(Manufactured):
    materials = RelationshipTo('Mat2DevAPI.models.matter.Material', "HAS_PART", model=hasPartRel)
    components = RelationshipTo('Mat2DevAPI.models.matter.Component', 'HAS_PART', model=hasPartRel)
    devices = RelationshipTo('Mat2DevAPI.models.matter.Device', 'HAS_PART', model=hasPartRel)
    pass
