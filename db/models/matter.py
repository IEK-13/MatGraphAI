from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
                      FloatProperty, UniqueIdProperty, RelationshipTo,
                      RelationshipFrom, StructuredRel)

from abstractclasses import *
from dataproperties import *

# Abstract Classes Containing Chemical and manufactured Entities


class Matter(CausalObject):
    isManufactured = RelationshipTo("Manufacturing", "isMeasurementInput",
                                    model=isManufacturingInput)
    isOutput = RelationshipFrom("Manufacturing", "isManufacturingOutput",
                                model=hasManufacturingOutput)
    measured = RelationshipTo("Measurement", "isMeasured",
                              model=isMeasured)


class ChemicalEntity(Matter):
    pass


class Molecule(ChemicalEntity):
    nAtoms = IntegerProperty()
    hasAtom = RelationshipTo("Atom", "hasPart", model=hasPart)
    pass


class Atom(ChemicalEntity):
    pass


class Manufactured(Matter):
    hasAtom = RelationshipTo("Atom", "hasPart", model=hasPart)
    pass


class ManufacturedMaterial(Manufactured):
    hasMolecule = RelationshipTo("Molecule", "hasPart", model=hasPart)
    pass


class ManufacturedComponent(Manufactured):
    hasMaterial = RelationshipTo("Material", "hasPart", model=hasPart)
    hasComponent = RelationshipTo("Component", "hasPart", model=hasPart)
    pass


class ManufacturedFuelCellComponent(ManufacturedComponent):
    pass


class ManufacturedDevice(Manufactured):
    hasMaterial = RelationshipTo("Material", "hasPart", model=hasPart)
    hasComponent = RelationshipTo("Component", "hasPart", model=hasPart)
    pass


# Manufactured components


class MEA(ManufacturedFuelCellComponent):
    pass


class CatalystLayer(ManufacturedFuelCellComponent):
    pass


class GDL(ManufacturedFuelCellComponent):
    pass


class Membrane(ManufacturedFuelCellComponent):
    pass


class BipolarPlate(ManufacturedFuelCellComponent):
    pass


class Seal(ManufacturedFuelCellComponent):
    pass


class CoolingPlate(ManufacturedFuelCellComponent):
    pass


# Materials Classes


class Catalyst(ManufacturedMaterial):
    pass


class CatalystInk(ManufacturedMaterial):
    pass


class Metal(ManufacturedMaterial):
    pass


class Composite(ManufacturedMaterial):
    pass


class CarbonBasedMaterial(ManufacturedMaterial):
    pass


class TransferSubstrate(ManufacturedMaterial):
    pass


# ManufacturedDevices


class FuelCell(ManufacturedDevice):
    hasMaterial = RelationshipTo("Material", "hasPart", model=hasPart)
    hasMEA = RelationshipTo("MEA", "hasPart", model=hasPart)
    hasSeal = RelationshipTo("Seal", "hasPart", model=hasPart)
    hasBipolarPlatePlate = RelationshipTo(
        "BipolarPlate", "hasPart", model=hasPart)
    pass


# Molecules


class Polymer(Molecule):
    pass


class Ionomer(Polymer):
    pass


class Solvent(Molecule):
    pass
