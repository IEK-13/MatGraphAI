from neomodel import (RelationshipTo,
                      StringProperty,
                      RelationshipFrom,
                      BooleanProperty,
                      OneOrMore,
                      ZeroOrMore
                      )

from Mat2DevAPI.models.abstractclasses import CausalObject
from Mat2DevAPI.models.matter import Material, Molecule, Component, Device
from Mat2DevAPI.models.relationships import hasParticipantRel, byResearcherRel, byDeviceRel, \
    hasFileOutputRel, isManufacturingInputRel, hasMeasurementOutputRel, hasPartRel, \
    isManufacturingOutputRel, isARel


class Process(CausalObject):
    # Organizational Data
    run_title = StringProperty(unique=True)
    run_id = StringProperty(unique=True)
    public_access = BooleanProperty()

    # Relationships
    is_a = RelationshipTo('Mat2DevAPI.models.ontology.EMMO_Process', "IS_A", model=isARel, cardinality=ZeroOrMore)
    parameter = RelationshipTo('Mat2DevAPI.models.properties.Parameter', "HAS_PARAMETER", model=hasParticipantRel, cardinality=ZeroOrMore)
    researcher = RelationshipTo('Mat2DevAPI.models.metadata.Researcher', "BY", model=byResearcherRel, cardinality=ZeroOrMore)
    instrument = RelationshipTo('Mat2DevAPI.models.metadata.Instrument', "BY_INSTRUMENT", model=byDeviceRel, cardinality=ZeroOrMore)
    subprocess_measurement = RelationshipTo("Measurement", "HAS_PART", model=hasPartRel, cardinality=ZeroOrMore)
    next_step_measurement = RelationshipTo("Measurement", "HAS_PART", model=hasPartRel, cardinality=ZeroOrMore)
    subprocess_manufacturing = RelationshipTo("Manufacturing", "HAS_PART", model=hasPartRel, cardinality=ZeroOrMore)
    next_step_manufacturing = RelationshipTo("Manufacturing", "HAS_PART", model=hasPartRel, cardinality=ZeroOrMore)
    publication = RelationshipTo('Mat2DevAPI.models.metadata.Publication', "PUBLISHED_IN", model=hasPartRel, cardinality=ZeroOrMore)
    institution = RelationshipTo('Mat2DevAPI.models.metadata.Institution', "PUBLISHED_IN", model=hasPartRel, cardinality=ZeroOrMore)
    __abstract_node__ = True

    class Meta:
        app_label = 'Mat2DevAPI'



class Manufacturing(Process):

    def __str__(self):
        if self.name:
            return f"Manufacturing {self.name} with uid {self.uid}"
        return f"Manufacturing with uid {self.uid}"

    material_output = RelationshipTo(Material, 'IS_MANUFACTURING_OUTPUT', model=isManufacturingOutputRel)
    molecule_output = RelationshipTo(Molecule, 'IS_MANUFACTURING_OUTPUT', model=isManufacturingOutputRel)
    component_output = RelationshipTo(Component, 'IS_MANUFACTURING_OUTPUT', model=isManufacturingOutputRel)
    device_output = RelationshipTo(Device, 'IS_MANUFACTURING_OUTPUT', model=isManufacturingOutputRel)

    material_input = RelationshipFrom('Mat2DevAPI.models.matter.Material', 'IS_MANUFACTURING_INPUT', model=isManufacturingInputRel,
                                      cardinality=ZeroOrMore)
    molecule_input = RelationshipFrom('Mat2DevAPI.models.matter.Molecule', "IS_MANUFACTURING_INPUT", model=isManufacturingInputRel,
                                      cardinality=ZeroOrMore)
    component_input = RelationshipFrom('Mat2DevAPI.models.matter.Component', "IS_MANUFACTURING_INPUT", model=isManufacturingInputRel,
                                       cardinality=ZeroOrMore)
    device_input = RelationshipFrom('Mat2DevAPI.models.matter.Device', "IS_MANUFACTURING_INPUT", model=isManufacturingInputRel,
                                    cardinality=ZeroOrMore)
    pass


class Measurement(Process):

    def __str__(self):
        return "Measurement " + self.uid

    # is_a = RelationshipTo(EMMOProcess, "IS_A", model=isARel)
    property_output = RelationshipTo('Mat2DevAPI.models.properties.Property', "HAS_MEASUREMENT_OUTPUT", model=hasMeasurementOutputRel,
                                     cardinality=OneOrMore)
    file_output = RelationshipTo('Mat2DevAPI.models.metadata.File', "HAS_FILE_OUTPUT", model=hasFileOutputRel, cardinality=ZeroOrMore)

    material_input = RelationshipFrom('Mat2DevAPI.models.matter.Material', 'IS_MEASUREMENT_INPUT', model=isManufacturingInputRel,
                                      cardinality=ZeroOrMore)
    molecule_input = RelationshipFrom('Mat2DevAPI.models.matter.Molecule', "IS_MEASUREMENT_INPUT", model=isManufacturingInputRel,
                                      cardinality=ZeroOrMore)
    component_input = RelationshipFrom('Mat2DevAPI.models.matter.Component', "IS_MEASUREMENT_INPUT", model=isManufacturingInputRel,
                                       cardinality=ZeroOrMore)
    device_input = RelationshipFrom('Mat2DevAPI.models.matter.Device', "IS_MEASUREMENT_INPUT", model=isManufacturingInputRel,
                                    cardinality=ZeroOrMore)