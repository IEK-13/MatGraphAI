from neomodel import (RelationshipTo,
                      StringProperty,
                      RelationshipFrom,
                      FloatProperty,
                      BooleanProperty
                      )
from django.db import models

from Mat2DevAPI.models.abstractclasses import CausalObject
from Mat2DevAPI.models.metadata import Researcher, Instrument
from Mat2DevAPI.models.relationships import inLocationRel, hasParticipantRel, byResearcherRel, byDeviceRel, \
    subProcessRel, hasFileOutputRel, isManufacturingInputRel, hasMeasurementOutputRel, hasParameterInputRel
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
    subProcess = RelationshipTo("SubProcess", subProcessRel, model=subProcessRel)
    isProcessMoleculeInput = RelationshipFrom(models.ForeignKey("Molecule",
                                                                on_delete=models.deletion.CASCADE),
                                              isManufacturingInputRel,
                                              model=isManufacturingInputRel)
    isProcessComponentInput = RelationshipFrom(models.ForeignKey("Component",
                                                                 on_delete=models.deletion.CASCADE),
                                               isManufacturingInputRel,
                                               model=isManufacturingInputRel)
    isProcessMaterialInput = RelationshipFrom(models.ForeignKey("Material",
                                                                on_delete=models.deletion.CASCADE),
                                              isManufacturingInputRel,
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
    pass


class Measurement(Process):
    type = StringProperty(choices=MEASUREMENT_TYPE_CHOICEFIELD)
    granularity_level = StringProperty(choices=GRANULARITY_TYPE_CHOICEFIELD)
    hasMeasurementOutput = RelationshipTo(models.ForeignKey("Property",
                                                            on_delete=models.deletion.CASCADE),
                                          hasMeasurementOutputRel,
                                          model=hasMeasurementOutputRel)
    hasFileOutput = RelationshipTo(models.ForeignKey("Property",
                                                     on_delete=models.deletion.CASCADE),
                                   hasFileOutputRel,
                                   model=hasFileOutputRel),


class Parameter(CausalObject):
    name = StringProperty(unique_index=True, required=True)
    value = FloatProperty()
    error = FloatProperty()
    parameter = RelationshipTo(Measurement, hasParameterInputRel,
                               model=hasParameterInputRel)
