from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
                      FloatProperty, UniqueIdProperty, RelationshipTo)

from abstractclasses import *


class Element(UniqueNamedNode):
    pass


class Material(Object):
    element = RelationshipTo(Element, 'CONSISTS_OF')


class Component(Object):
    component = RelationshipTo(Material, 'CONSISTS_OF')


class Device(Object):
    component = RelationshipTo(Component, 'CONSISTS_OF')


class MEA(Component):
    pass


class CatalystLayer(Component):
    pass


class GDL(Component):
    pass


class CoatingSubstrate(Material):
    pass


class Catalyst(Material):
    pass


class CatalystInk(Material):
    pass


class Ionomer(Material):
    pass


class TransferSubstrate(Material):
    pass


class FuelCell(Device):
    pass
