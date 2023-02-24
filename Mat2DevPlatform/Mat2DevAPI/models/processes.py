from neomodel import (RelationshipTo,
                      StringProperty,
                      RelationshipFrom,
                      FloatProperty,
                      BooleanProperty
                      )
from django.db import models

from Mat2DevAPI.models.abstractclasses import CausalObject
from Mat2DevAPI.models.matter import Material
from Mat2DevAPI.models.metadata import Researcher, Instrument
from Mat2DevAPI.models.ontology import EMMO_Process
from Mat2DevAPI.models.relationships import inLocationRel, hasParticipantRel, byResearcherRel, byDeviceRel, \
    subProcessRel, hasFileOutputRel, isManufacturingInputRel, hasMeasurementOutputRel, hasParameterInputRel, hasPartRel, \
    isManufacturingOutputRel, isARel
from Mat2DevAPI.choices.ChoiceFields import GRANULARITY_TYPE_CHOICEFIELD, MEASUREMENT_TYPE_CHOICEFIELD


class Process(CausalObject):
    # Organizational Data
    run_title = StringProperty(unique=True)
    run_id = StringProperty(unique=True)
    sample_id = StringProperty(unique=True)
    Institution = StringProperty(unique=True)
    public_access = BooleanProperty()

    # Relationships
    participant = RelationshipTo(
        "Parameter", hasParticipantRel, model=hasParticipantRel)
    researcher = RelationshipTo(Researcher, byResearcherRel, model=byResearcherRel)
    instrument = RelationshipTo(Instrument, byDeviceRel)
    hasSubprocess          = RelationshipFrom(models.ForeignKey("Process",
                            on_delete=models.deletion.CASCADE),
                            hasPartRel,
                            model=hasPartRel)
    isProcessMoleculeInput = RelationshipFrom(models.ForeignKey("Molecule",
                            on_delete=models.deletion.CASCADE),
                            isManufacturingInputRel,
                            model=isManufacturingInputRel)
    isProcessComponentInput = RelationshipFrom(models.ForeignKey("Component",
                                                                 on_delete=models.deletion.CASCADE),
                                               isManufacturingInputRel,
                                               model=isManufacturingInputRel)
    material_input = RelationshipFrom(Material,
                                      'IS_MANUFACTURING_INPUT',
                                              model=isManufacturingInputRel)

    inCountry = RelationshipTo(models.ForeignKey("Country", on_delete=models.deletion.CASCADE),
                               inLocationRel, model=inLocationRel)
    inCity = RelationshipTo(models.ForeignKey("City", on_delete=models.deletion.CASCADE),
                            inLocationRel, model=inLocationRel)
    inInstitution = RelationshipTo(models.ForeignKey("Institution", on_delete=models.deletion.CASCADE),
                                   inLocationRel, model=inLocationRel)

    __abstract_node__ = True

    class Meta:
        app_label = 'Mat2DevAPI'


class SubProcess(Process):
    __abstract_node__ = True


# Manufacturing Classes


class Manufacturing(Process):

    is_a = RelationshipTo(EMMO_Manufacturing, "IS_A", model=isARel)
    def  __str__(self):
        print(self.is_a)
        return  "test"
    material_output = RelationshipTo(Material,
                                       'IS_MANUFACTURING_OUTPUT',
                                       model=isManufacturingOutputRel)
    pass


class Measurement(Process):
    is_a = RelationshipTo(EMMO_Measurement, "IS_A", model=isARel)
    type = StringProperty(choices=MEASUREMENT_TYPE_CHOICEFIELD)
    hasMeasurementOutput = RelationshipTo(models.ForeignKey("Property",
                                                            on_delete=models.deletion.CASCADE),
                                          hasMeasurementOutputRel,
                                          model=hasMeasurementOutputRel)
    hasFileOutput = RelationshipTo(models.ForeignKey("Property",
                                                     on_delete=models.deletion.CASCADE),
                                   hasFileOutputRel,
                                   model=hasFileOutputRel),


