from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
                      FloatProperty, UniqueIdProperty, RelationshipTo, DateTimeProperty,
                      StructuredRel)

from matter import *
from abstractclasses import *
from properties import (Property)


class Process(Physical):
    uid = UniqueIdProperty()
    year = DateTimeProperty()
    participant = RelationshipTo("Parameter", hasParticipant)
    researcher = RelationshipTo("Researcher", byResearcher)
    instrument = RelationshipTo("Instrument", byDevice)
    __abstract_node__ = True


class Manufacturing(Process):
    processed = RelationshipFrom(Engineered, processed)
    fabricates = RelationshipTo(Engineered, fabricates)
    pass


class Measurement(Process):
    property = RelationshipTo(Property, yieldsQuant)
    pass


class Parameter(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    value = FloatProperty()
    error = FloatProperty()
