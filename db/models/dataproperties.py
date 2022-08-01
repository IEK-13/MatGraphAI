from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
                      FloatProperty, UniqueIdProperty, RelationshipTo,
                      RelationshipFrom, StructuredRel)

from abstractclasses import *


class hasPart(StructuredRel):
    pass


class isPart(StructuredRel):
    __abstract_node = True


class hasDirectPart(StructuredRel):
    __abstract_node = True
    pass


# DirectPart properties


class subProcess(hasDirectPart):
    pass


class hasComponent(hasDirectPart):
    pass


class hasAtom(hasDirectPart):
    n = IntegerProperty()
    pass

# MoleculePart properties


class hasMolecule(hasDirectPart):
    pass


class hasIonomer(hasMolecule):
    pass


class hasSolvent(hasMolecule):
    pass


class hasSolute(hasMolecule):
    pass


# MaterialPart Properties


class hasMaterial(hasDirectPart):
    pass


class hasActiveMaterial(hasMaterial):
    __abstract_node = True
    pass


class hasCatalyst(hasActiveMaterial):
    pass


class hasCatalystInk(hasMaterial):
    pass


# isParticipant properties


class isParticipant(isPart):
    pass


class isProcessInput(isParticipant):
    pass

# isProcessInput Properties


class isProcessInput(isParticipant):
    pass


class isManufacturingInput(isProcessInput):
    pass


class isMeasurementInput(isProcessInput):
    pass


class isMeasured(isMeasurementInput):
    pass


# hasParticipant Properties


class hasParticipant(hasPart):
    pass


class hasParameterInput(hasParticipant):
    pass

# hasProcessOutput properties


class hasProcessOutput(hasParticipant):
    pass


class hasManufacturingOutput(hasProcessOutput):
    pass


class hasMeasurementOutput(hasProcessOutput):
    pass


class byResearcher(hasParticipant):
    pass


class byDevice(hasParticipant):
    pass
