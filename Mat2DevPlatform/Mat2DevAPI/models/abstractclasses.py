from abc import ABC, ABCMeta

from neomodel import (StructuredNode, StringProperty, UniqueIdProperty, DateTimeProperty)
from django_neomodel import DjangoNode

class NamedNode(DjangoNode):
    @classmethod
    def category(cls):
        pass

    date_added = DateTimeProperty(required=True)
    name = StringProperty()
    __abstract_node__ = True


class UniqueNamedNode(NamedNode):
    uid = UniqueIdProperty()
    __abstract_node__ = True


class UniqueNode(DjangoNode):
    @classmethod
    def category(cls):
        pass

    date_added = DateTimeProperty(required=True)
    uid = UniqueIdProperty()
    __abstract_node__ = True


class CausalObject(UniqueNamedNode):
    type = StringProperty()
    __abstract_node__ = True
