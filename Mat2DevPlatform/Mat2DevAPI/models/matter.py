from neomodel import IntegerProperty, StringProperty, ZeroOrMore
from neomodel import RelationshipTo, RelationshipFrom

from Mat2DevAPI.models.abstractclasses import CausalObject, UIDDjangoNode
from Mat2DevAPI.models.relationships import (HasPartRel, HasMeasurementOutputRel,
                                             IsManufacturingOutputRel,
                                             IsManufacturingInputRel,
                                             IsARel, HasPropertyRel)

class Matter(CausalObject):
    """
    Abstract base class representing matter in the knowledge graph.
    """
    # properties = RelationshipTo('Mat2DevAPI.models.properties.Property', 'HAS_PROPERTY', model=HasPropertyRel,
    #                             cardinality=ZeroOrMore)
    # is_a = RelationshipTo('Mat2DevAPI.models.ontology.EMMO_Matter', 'IS_A', cardinality=ZeroOrMore, model=IsARel)
    # manufacturing_input = RelationshipTo('Mat2DevAPI.models.processes.Manufacturing', 'IS_MANUFACTURING_INPUT',
    #                                      model=IsManufacturingInputRel)
    # manufacturing_output = RelationshipFrom('Mat2DevAPI.models.processes.Manufacturing', 'IS_MANUFACTURING_OUTPUT',
    #                                         model=IsManufacturingOutputRel)
    # measurement_input = RelationshipTo('Mat2DevAPI.models.processes.Measurement', 'IS_MEASUREMENT_INPUT',
    #                                    model=HasMeasurementOutputRel)
    __abstract_node__ = True


class Manufactured(Matter):
    """
    Abstract class representing manufactured matter.
    """
    # elements = RelationshipTo('Mat2DevAPI.models.matter.Element', "HAS_PART", model=HasPartRel)
    # molecules = RelationshipTo('Mat2DevAPI.models.matter.Molecule', "HAS_PART", model=HasPartRel)
    __abstract_node__ = True


class Element(Matter):
    """
    Class representing an element in the knowledge graph.
    """
    name = StringProperty(unique_index=True, required=True)
    summary = StringProperty()
    symbol = StringProperty(required=True, unique_index=True)

    elements = RelationshipFrom('Mat2DevAPI.models.matter.Manufactured', "HAS_PART", model=HasPartRel)


class Molecule(UIDDjangoNode):
    """
    Class representing a molecule in the knowledge graph.
    """

    # class Meta(UIDDjangoNode.Meta):
    #     pass

    # Identifiers
    # SMILES = StringProperty()
    # InChI_key = StringProperty()
    # InChI = StringProperty()
    # compound_cid = IntegerProperty()
    # IUPAC_name = StringProperty()
    # chemical_formula = StringProperty()
    # CAS = StringProperty()
    pass


class Material(Manufactured):
    """
    Class representing a material in the knowledge graph.
    """
    sum_formula = StringProperty()
    materials = RelationshipTo('Mat2DevAPI.models.matter.Material', "HAS_PART", model=HasPartRel)
    material_output = RelationshipTo("Mat2DevAPI.models.processes.Process", 'IS_MANUFACTURING_OUTPUT',
                                     model=IsManufacturingOutputRel)
    molecules = RelationshipFrom('Mat2DevAPI.models.matter.Material', "HAS_PART", model=HasPartRel)


class Component(Manufactured):
    """
    Class representing a component in the knowledge graph.
    """
    materials = RelationshipTo('Mat2DevAPI.models.matter.Material', "HAS_PART", model=HasPartRel)
    components = RelationshipTo('Mat2DevAPI.models.matter.Component', 'HAS_PART', model=HasPartRel)
    material = RelationshipFrom('Mat2DevAPI.models.matter.Component', "HAS_PART", model=HasPartRel)


class Device(Manufactured):
    """
    Class representing a device in the knowledge graph.
    """
    materials = RelationshipTo('Mat2DevAPI.models.matter.Material', "HAS_PART", model=HasPartRel)
    components = RelationshipTo('Mat2DevAPI.models.matter.Component', 'HAS_PART', model=HasPartRel)
    devices = RelationshipTo('Mat2DevAPI.models.matter.Device', 'HAS_PART', model=HasPartRel)
    pass
