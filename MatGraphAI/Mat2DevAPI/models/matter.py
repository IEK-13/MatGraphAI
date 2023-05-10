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

    properties: A relationship to properties of the matter.
    is_a: A relationship to ontology classes this matter is an instance of.
    manufacturing_input: A relationship to manufacturing processes where the matter is an input.
    manufacturing_output: A relationship from manufacturing processes where the matter is an output.
    measurement_input: A relationship to measurement processes where the matter is an input.
    """
    properties = RelationshipTo('Mat2DevAPI.models.properties.Property', 'HAS_PROPERTY', model=HasPropertyRel,
                                cardinality=ZeroOrMore)
    is_a = RelationshipTo('Mat2DevAPI.models.ontology.EMMOMatter', 'IS_A', cardinality=ZeroOrMore, model=IsARel)
    manufacturing_input = RelationshipTo('Mat2DevAPI.models.processes.Manufacturing', 'IS_MANUFACTURING_INPUT',
                                         model=IsManufacturingInputRel)
    manufacturing_output = RelationshipFrom('Mat2DevAPI.models.processes.Manufacturing', 'IS_MANUFACTURING_OUTPUT',
                                            model=IsManufacturingOutputRel)
    measurement_input = RelationshipTo('Mat2DevAPI.models.processes.Measurement', 'IS_MEASUREMENT_INPUT',
                                       model=HasMeasurementOutputRel)
    __abstract_node__ = True


class Manufactured(Matter):
    """
    Abstract class representing manufactured matter.


    elements: A relationship to elements that the manufactured matter has as parts.
    molecules: A relationship to molecules that the manufactured matter has as parts.
    """
    elements = RelationshipTo('Mat2DevAPI.models.matter.Element', "HAS_PART", model=HasPartRel)
    molecules = RelationshipTo('Mat2DevAPI.models.matter.Molecule', "HAS_PART", model=HasPartRel)
    __abstract_node__ = True


class Element(Matter):
    """
    Class representing an element in the knowledge graph.


    name: The name of the element.
    summary: A brief description of the element.
    symbol: The chemical symbol for the element.
    elements: A relationship from manufactured matter that has the element as a part.
    """
    name = StringProperty(unique_index=True, required=True)
    summary = StringProperty()
    symbol = StringProperty(required=True, unique_index=True)

    elements = RelationshipFrom('Mat2DevAPI.models.matter.Manufactured', "HAS_PART", model=HasPartRel)


class Molecule(UIDDjangoNode):
    """
    Abstract base class representing matter in the knowledge graph.


    properties: A relationship to properties of the matter.
    is_a: A relationship to ontology classes this matter is an instance of.
    manufacturing_input: A relationship to manufacturing processes where the matter is an input.
    manufacturing_output: A relationship from manufacturing processes where the matter is an output.
    measurement_input: A relationship to measurement processes where the matter is an input.
    """

    class Meta(UIDDjangoNode.Meta):
        pass

    # Identifiers
    SMILES = StringProperty()
    InChI_key = StringProperty()
    InChI = StringProperty()
    compound_cid = IntegerProperty()
    IUPAC_name = StringProperty()
    chemical_formula = StringProperty()
    CAS = StringProperty()
    pass


class Material(Manufactured):
    """
    Class representing a material in the knowledge graph.

    sum_formula: The overall chemical formula of the material.
    materials: A relationship to materials that the material has as parts.
    material_output: A relationship to processes that have the material as a manufacturing output.
    molecules: A relationship from materials that have the material as a part.
    """
    sum_formula = StringProperty()
    materials = RelationshipTo('Mat2DevAPI.models.matter.Material', "HAS_PART", model=HasPartRel)
    material_output = RelationshipTo("Mat2DevAPI.models.processes.Process", 'IS_MANUFACTURING_OUTPUT',
                                     model=IsManufacturingOutputRel)
    molecules = RelationshipFrom('Mat2DevAPI.models.matter.Material', "HAS_PART", model=HasPartRel)


class Component(Manufactured):
    """
    Class representing a component in the knowledge graph.

    materials: A relationship to materials that the component has as parts.
    components: A relationship to components that the component has as parts.
    material: A relationship from components that have the component as a part.
    """
    materials = RelationshipTo('Mat2DevAPI.models.matter.Material', "HAS_PART", model=HasPartRel)
    components = RelationshipTo('Mat2DevAPI.models.matter.Component', 'HAS_PART', model=HasPartRel)
    material = RelationshipFrom('Mat2DevAPI.models.matter.Component', "HAS_PART", model=HasPartRel)


class Device(Manufactured):
    """
    Class representing a device in the knowledge graph.

    materials: A relationship to materials that the device has as parts.
    components: A relationship to components that the device has as parts.
    devices: A relationship to devices that the device has as parts.
    """
    materials = RelationshipTo('Mat2DevAPI.models.matter.Material', "HAS_PART", model=HasPartRel)
    components = RelationshipTo('Mat2DevAPI.models.matter.Component', 'HAS_PART', model=HasPartRel)
    devices = RelationshipTo('Mat2DevAPI.models.matter.Device', 'HAS_PART', model=HasPartRel)
    pass
