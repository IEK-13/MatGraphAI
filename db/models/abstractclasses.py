from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
                      FloatProperty, UniqueIdProperty, RelationshipTo, ArrayProperty,
                      DateTimeProperty, StructuredRel)


class NamedNode(StructuredNode):
    name = StringProperty(required=True)
    __abstract_node__ = True


class UniqueNamedNode(NamedNode):
    uid = UniqueIdProperty()
    __abstract_node__ = True


class UniqueNode(StructuredNode):
    uid = UniqueIdProperty()
    __abstract_node__ = True


class CausalObject(UniqueNamedNode):
    type = StringProperty()
    __abstract_node__ = True
