from abc import ABC
from .abstractclasses import *
from neomodel import (StructuredNode, StringProperty)


class Instrument(UniqueNode):
    instrument = StringProperty(unique_index=True, required=True)
    model = StringProperty(unique_index=True, required=True)


class Researcher(UniqueNode):
    name = StringProperty(unique_index=True, required=True)
    Facility = StringProperty(unique_index=True, required=True)
