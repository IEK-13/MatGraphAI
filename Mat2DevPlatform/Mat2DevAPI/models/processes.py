from .dataproperties import *
from .matter import *


class Process(CausalObject):
    uid = UniqueIdProperty()
    date = DateTimeProperty()
    participant = RelationshipTo(
        "Parameter", hasParticipant, model=hasParticipant)
    researcher = RelationshipTo("Researcher", byResearcher, model=byResearcher)
    instrument = RelationshipTo("Instrument", byDevice)
    subProcess = RelationshipTo("SubProcess", "subProcess", model=subProcess)
    __abstract_node__ = True

    class Meta:
        app_label = 'Mat2DevAPI'


class SubProcess(Process):
    __abstract_node__ = True


# Manufacturing Classes


class Manufacturing(Process):
    isManufacturingMoleculeInput = RelationshipFrom("Molecule", "isManufacturingInput",
                                                    model=isManufacturingInput)
    isManufacturingComponentInput = RelationshipFrom("Component", "isManufacturingInput",
                                                     model=isManufacturingInput)
    isManufacturingMaterialInput = RelationshipFrom("Material", "isManufacturingInput",
                                                    model=isManufacturingInput)
    pass


class FuelCellManufacturing(Manufacturing):
    pass


class Measurement(Process):
    hasMeasurementOutput = RelationshipTo(ForeignKey("Property", on_delete=CASCADE, verbose_name='Property Details'),
                                          "hasMeasurementOutput",
                                          model=hasMeasurementOutput)
    ComponentInput = RelationshipFrom("Component", "isMeasured",
                                      model=isMeasured)
    DeviceInput = RelationshipFrom("Material", "isMeasured",
                                   model=isMeasured)
    MaterialInput = RelationshipFrom("Material", "isMeasured",
                                     model=isMeasured)
    pass


class Parameter(DjangoNode):
    name = StringProperty(unique_index=True, required=True)
    value = FloatProperty()
    error = FloatProperty()
    parameter = RelationshipTo(Measurement, "hasParameterInput",
                               model=hasParameterInput)
