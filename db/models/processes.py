from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
                      FloatProperty, UniqueIdProperty, RelationshipTo, DateTimeProperty)

from compositions import *
from abstractclasses import *
from properties import (Property)


class FabricationProcess(Process):
    material = RelationshipTo(Material, "YIELDS_MAT")
    component = RelationshipTo(Component, "YIELDS_COMP")
    device = RelationshipTo(Device, "YIELDS_DEV")
    pass


class Parameter(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    value = FloatProperty()
    error = FloatProperty()
