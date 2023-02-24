from django.db import models
from neomodel import (RelationshipTo,
                      StringProperty,
                      RelationshipFrom,
                      BooleanProperty
                      )

from Mat2DevAPI.choices.ChoiceFields import MEASUREMENT_TYPE_CHOICEFIELD
from Mat2DevAPI.models.abstractclasses import CausalObject
from Mat2DevAPI.models.matter import Material
from Mat2DevAPI.models.metadata import Researcher, Instrument
from Mat2DevAPI.models.ontology import EMMOProcess
from Mat2DevAPI.models.relationships import inLocationRel, hasParticipantRel, byResearcherRel, byDeviceRel, \
    hasFileOutputRel, isManufacturingInputRel, hasMeasurementOutputRel, hasPartRel, \
    isManufacturingOutputRel, isARel


class Process(CausalObject):
    is_a = RelationshipTo(EMMOProcess,
                          "IS_A",
                          model=isARel)
    # Organizational Data
    run_title = StringProperty(unique=True)
    run_id = StringProperty(unique=True)
    sample_id = StringProperty(unique=True)
    Institution = StringProperty(unique=True)
    public_access = BooleanProperty()

    # Relationships
    # participant = RelationshipTo("Parameter", "HAS_PARAMETER", model=hasParticipantRel)
    # researcher = RelationshipTo(Researcher, "BY", model=byResearcherRel)
    # instrument = RelationshipTo(Instrument, "BY_INSTRUMENT", byDeviceRel)
    # hasSubprocess = RelationshipFrom(models.ForeignKey("Process", on_delete=models.deletion.CASCADE),
    #                                  hasPartRel,
    #                                  model=hasPartRel)
    # isProcessMoleculeInput = RelationshipFrom(models.ForeignKey("Molecule", on_delete=models.deletion.CASCADE),
    #                                           isManufacturingInputRel,
    #                                           model=isManufacturingInputRel)
    # isProcessComponentInput = RelationshipFrom(models.ForeignKey("Component", on_delete=models.deletion.CASCADE),
    #                                            isManufacturingInputRel,
    #                                            model=isManufacturingInputRel)
    # material_input = RelationshipFrom(Material,
    #                                   'IS_MANUFACTURING_INPUT',
    #                                   model=isManufacturingInputRel)
    #
    # inCountry = RelationshipTo(models.ForeignKey("Country", on_delete=models.deletion.CASCADE),
    #                            inLocationRel,
    #                            model=inLocationRel)
    # inCity = RelationshipTo(models.ForeignKey("City", on_delete=models.deletion.CASCADE),
    #                         inLocationRel,
    #                         model=inLocationRel)
    # inInstitution = RelationshipTo(models.ForeignKey("Institution", on_delete=models.deletion.CASCADE),
    #                                inLocationRel,
    #                                model=inLocationRel)
    __abstract_node__ = True

    class Meta:
        app_label = 'Mat2DevAPI'


class SubProcess(Process):
    __abstract_node__ = True


# Manufacturing Classes


class Manufacturing(Process):

    # is_a = RelationshipTo(EMMOProcess, "IS_A", model=isARel)

    def __str__(self):
        return "Manufacturing " + self.uid

    material_output = RelationshipTo(Material,
                                     'IS_MANUFACTURING_OUTPUT',
                                     model=isManufacturingOutputRel)
    pass


class Measurement(Process):

    def __str__(self):
        return "Measurement " + self.uid

    # is_a = RelationshipTo(EMMOProcess, "IS_A", model=isARel)
    type = StringProperty(choices=MEASUREMENT_TYPE_CHOICEFIELD)
    hasMeasurementOutput = RelationshipTo(models.ForeignKey("Property", on_delete=models.deletion.CASCADE),
                                          hasMeasurementOutputRel,
                                          model=hasMeasurementOutputRel)
    hasFileOutput = RelationshipTo(models.ForeignKey("Property", on_delete=models.deletion.CASCADE),
                                   hasFileOutputRel,
                                   model=hasFileOutputRel),
