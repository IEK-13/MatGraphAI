from neomodel import StructuredRel, IntegerProperty, BooleanProperty, StringProperty


class byResearcherRel(StructuredRel):
    CONTRIBUTION_LABEL_COICES = {'first_author': 'First Author',
                                 'author': 'Author',
                                 'conducted_experiment': 'Conducted Experiment',
                                 'instrument_scientist': 'Instrument Scientist',
                                 'contributor': 'Contributor',
                                 'planned_experiment': 'Planned Experiment'}
    label = StringProperty(choices=CONTRIBUTION_LABEL_COICES,
                           default='contributor'
                           )

class inLocationRel(StructuredRel):
    test = StringProperty()




class hasPartRel(StructuredRel):
    pass


class isPartRel(StructuredRel):
    __abstract_node = True


class hasDirectPartRel(StructuredRel):
    __abstract_node = True
    pass


# DirectPart properties


class subProcessRel(hasDirectPartRel):
    pass


class hasComponentRel(hasDirectPartRel):
    pass


class hasAtomRel(hasDirectPartRel):
    n = IntegerProperty()
    pass


# MoleculePart properties


class hasMoleculeRel(hasDirectPartRel):
    pass


class hasIonomerRel(hasMoleculeRel):
    pass


class hasSolventRel(hasMoleculeRel):
    pass


class hasSoluteRel(hasMoleculeRel):
    pass


# MaterialPart Properties


class hasMaterialRel(hasDirectPartRel):
    pass


class hasActiveMaterialRel(hasMaterialRel):
    __abstract_node = True
    pass


class hasCatalystRel(hasActiveMaterialRel):
    pass


class hasCatalystInkRel(hasMaterialRel):
    pass


# isParticipant properties


class isParticipantRel(isPartRel):
    pass


class isProcessInputRel(isParticipantRel):
    pass


# isProcessInput Properties


class isManufacturingInputRel(isProcessInputRel):
    pass

class isManufacturingOutputRel(isProcessInputRel):
    pass

class isMeasurementInputRel(isProcessInputRel):
    pass


class isMeasuredRel(isMeasurementInputRel):
    pass


# hasParticipant Properties


class hasParticipantRel(hasPartRel):
    pass


class hasParameterInputRel(hasParticipantRel):
    pass


# hasProcessOutput properties


class hasProcessOutputRel(hasParticipantRel):
    pass


class hasManufacturingOutputRel(hasProcessOutputRel):
    pass


class hasMeasurementOutputRel(hasProcessOutputRel):
    pass

class hasFileOutputRel(hasProcessOutputRel):
    pass

class byResearcherRel(hasParticipantRel):
    pass


class byDeviceRel(hasParticipantRel):
    pass

class emmoIsA(StructuredRel):
    pass

class isARel(StructuredRel):
    pass