from properties import (Property)
from dataproperties import *
from abstractclasses import *
from matter import *
from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
                      FloatProperty, UniqueIdProperty, RelationshipTo, DateTimeProperty,
                      StructuredRel)


class Process(CausalObject):
    uid = UniqueIdProperty()
    date = DateTimeProperty()
    participant = RelationshipTo(
        "Parameter", hasParticipant, model=hasParticipant)
    researcher = RelationshipTo("Researcher", byResearcher, model=byResearcher)
    instrument = RelationshipTo("Instrument", byDevice)
    subProcess = RelationshipTo("SubProcess", "subProcess", model=subProcess)
    __abstract_node__ = True


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

# BipolarPlateManufacturing Classes


class BipolarPlateManufacturing(FuelCellManufacturing):
    isMaterialInput = RelationshipFrom("Material", "isManufacturingInput",
                                       model=isManufacturingInput)
    hasManufacturingOutput = RelationshipTo("BipolarPlate", "hasManufacturingOutput",
                                            model=hasManufacturingOutput)
    pass


class CoatedMetallicPlateManufacturing(BipolarPlateManufacturing):
    isMetalInput = RelationshipFrom("Metal", "isManufacturingInput",
                                    model=isManufacturingInput)
    pass


class CompositePlateManufacturing(BipolarPlateManufacturing):
    isCompositeInput = RelationshipFrom("Composite", "isManufacturingInput",
                                        model=isManufacturingInput)
    pass


class CarbonBasedCompositePlateManufacturing(CompositePlateManufacturing):
    isCarbonInput = RelationshipFrom("CarbonBasedMaterial", "isManufacturingInput",
                                     model=isManufacturingInput)
    pass


class MetalBasedCompositePlateManufacturing(CompositePlateManufacturing):
    isMetalInput = RelationshipFrom("Metal", "isManufacturingInput",
                                    model=isManufacturingInput)
    pass


class NonPorousGraphitePlateManufacturing(BipolarPlateManufacturing):
    isCarbonInput = RelationshipFrom("CarbonBasedMaterial", "isManufacturingInput",
                                     model=isManufacturingInput)
    pass


class MoldingWithFlowFieldsManufacturing(NonPorousGraphitePlateManufacturing):
    pass


class FlatPlateMoldingManufacturing(NonPorousGraphitePlateManufacturing):
    pass


# CatalystLayerManufacturing Classes


class CatalystLayerManufacturing(FuelCellManufacturing):
    hasManufacturingOutput = RelationshipTo("CatalystLayer", "hasManufacturingOutput",
                                            model=hasManufacturingOutput)
    isCatalystInkInput = RelationshipFrom("CatalystInk", "isManufacturingInput",
                                          model=isManufacturingInput)
    isCatalystInput = RelationshipFrom("Catalyst", "isManufacturingInput",
                                       model=isManufacturingInput)
    isIonomerInput = RelationshipFrom("Ionomer", "isManufacturingInput",
                                      model=isManufacturingInput)
    isSolventInput = RelationshipFrom("Solvent", "isManufacturingInput",
                                      model=isManufacturingInput)
    pass


# FuelCellAssembly Classes


class FuelCellAssembly(FuelCellManufacturing):
    hasManufacturingOutput = RelationshipTo("FuelCell", "hasManufacturingOutput",
                                            model=hasManufacturingOutput)
    isMEAInput = RelationshipFrom("MEA", "isManufacturingInput",
                                  model=isManufacturingInput)
    isBipolarPlateInput = RelationshipFrom("BipolarPlate", "isManufacturingInput",
                                           model=isManufacturingInput)
    isCoolingPlateInput = RelationshipFrom("CoolingPlate", "isManufacturingInput",
                                           model=isManufacturingInput)
    isSealInput = RelationshipFrom("Seal", "isManufacturingInput",
                                   model=isManufacturingInput)
    pass


# GDLManufacturing Classes


class GDLManufacturing(FuelCellManufacturing):
    hasManufacturingOutput = RelationshipTo("GDL", "hasManufacturingOutput",
                                            model=hasManufacturingOutput)
    pass


class CarbonClothManufacturing(GDLManufacturing):
    pass


class CarbonPaperManufacturing(GDLManufacturing):
    pass


# MEAManufacturing Classes


class MEAManufacturing(FuelCellManufacturing):
    hasManufacturingOutput = RelationshipTo("MEA", "hasManufacturingOutput",
                                            model=hasManufacturingOutput)
    isCatalystLayerInput = RelationshipFrom("CatalystLayer", "isManufacturingInput",
                                            model=isManufacturingInput)
    isGDLInput = RelationshipFrom("GDL", "isManufacturingInput",
                                  model=isManufacturingInput)
    isMembraneInput = RelationshipFrom("Membrane", "isManufacturingInput",
                                       model=isManufacturingInput)
    pass


class GDLCatalystAssembly(MEAManufacturing):
    pass


class MembraneCatalystAssembly(MEAManufacturing):
    pass


# MembraneManufacturing abstractclasses


class MembraneManufacturing(FuelCellManufacturing):
    hasManufacturingOutput = RelationshipTo("Membrane", "hasManufacturingOutput",
                                            model=hasManufacturingOutput)
    isPolymerInput = RelationshipFrom("Polymer", "isManufacturingInput",
                                      model=isManufacturingInput)
    pass


class GoreSelectMembraneSynthesis(MembraneManufacturing):
    pass


# ManufacturingSubProcesses Classes


class ManufacturingSubProcess(SubProcess):
    pass


class ChemicalReaction(ManufacturingSubProcess):
    pass


class FormingManufacturing(ManufacturingSubProcess):
    pass


class ContinuumManufacturing(ManufacturingSubProcess):
    pass


class DiscreteManufacturing(ManufacturingSubProcess):
    pass


class PurificationProcess(ManufacturingSubProcess):
    pass


class SubtractiveManufacturing(ManufacturingSubProcess):
    pass


# Measurement Classes


class Measurement(Process):
    hasMeasurementOutput = RelationshipTo("Property", "hasMeasurementOutput",
                                          model=hasMeasurementOutput)
    ComponentInput = RelationshipFrom("Component", "isMeasured",
                                        model=isMeasured)
    DeviceInput = RelationshipFrom("Material", "isMeasured",
                                     model=isMeasured)
    MaterialInput = RelationshipFrom("Material", "isMeasured",
                                       model=isMeasured)
    pass


class ElectricCurrentMeasurement(Measurement):
    hasElectricCurrentOutput = RelationshipTo("ElectricalProperty", "hasMeasurementOutput",
                                              model=hasMeasurementOutput)
    pass


class ElectricPotentialMeasurement(Measurement):
    hasElectricPotentialOutput = RelationshipTo("ElectricalProperty", "hasMeasurementOutput",
                                                model=hasMeasurementOutput)
    pass


class FuelCellMeasurement(Measurement):
    pass


class FuelCellComponentMeasurement(Measurement):
    pass


class Parameter(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    value = FloatProperty()
    error = FloatProperty()
    parameter = RelationshipTo(Measurement, "hasParameterInput",
                               model=hasParameterInput)
