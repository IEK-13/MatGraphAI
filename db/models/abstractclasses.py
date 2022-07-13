from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
                      FloatProperty, UniqueIdProperty, RelationshipTo, ArrayProperty,
                      DateTimeProperty, StructuredRel)


class hasPart(StructuredRel):
    name = "hasPart"
    pass


class hasParticipant(hasPart):
    name = "hasParticipant"
    pass


class processed(hasParticipant):
    name = "processes"
    pass


class measured(hasParticipant):
    name = "measured"
    pass


class usesParameter(hasParticipant):
    name = "usesParameter"
    pass


class byResearcher(hasParticipant):
    name = "byResearcher"
    pass


class byDevice(hasParticipant):
    pass


class yields(StructuredRel):
    name = "yields"
    pass


class fabricates(yields):
    name = "fabricates"
    pass


class yieldsQuant(yields):
    name = "yieldsQuant"
    pass


class NamedNode(StructuredNode):
    name = StringProperty(required=True)
    __abstract_node__ = True


class UniqueNamedNode(NamedNode):
    uid = UniqueIdProperty()
    __abstract_node__ = True


class UniqueNode(StructuredNode):
    name = UniqueIdProperty()
    __abstract_node__ = True


class Physical(UniqueNode):
    __abstract_node__ = True


class Virtual(UniqueNode):
    __abstract_node__ = True
