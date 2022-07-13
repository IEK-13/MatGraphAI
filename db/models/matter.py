from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
                      FloatProperty, UniqueIdProperty, RelationshipTo,
                      RelationshipFrom, StructuredRel)

from abstractclasses import *


class hasPart(StructuredRel):
    name = "hasPart"


class Matter(Physical):
    name = StringProperty()
    measured = RelationshipTo("Measurement", "hasMeasurementParticipant")
    consist = RelationshipTo("Matter", "hasPart")
    __abstract_node__ = True


class Engineered(Matter):
    processeduct = RelationshipTo(
        "Manufacturing", "isManufacturingParticipant")
    processproduct = RelationshipFrom("Manufacturing", "yieldsProduct")
    __abstract_node__ = True


class EngineeredMaterial(Engineered):
    __abstract_node__ = True


class EngineeredComponent(Engineered):
    __abstract_node__ = True


class EngineeredDevice(Engineered):
    __abstract_node__ = True


class Molecule(Matter):
    nAtoms = IntegerProperty()
    pass


class Atom(Matter):
    hasPart = RelationshipTo(Molecule, hasPart)
    pass


class MEA(EngineeredComponent):
    pass


class CatalystLayer(EngineeredComponent):
    pass


class GDL(EngineeredComponent):
    pass


class CoatingSubstrate(EngineeredMaterial):
    pass


class Catalyst(EngineeredMaterial):
    pass


class CatalystInk(EngineeredMaterial):
    pass


class Ionomer(EngineeredMaterial):
    pass


class TransferSubstrate(EngineeredMaterial):
    pass


class FuelCell(EngineeredDevice):
    pass
