from .abstractclasses import *


class Instrument(UniqueNode):
    class Meta:
        app_label = 'Mat2DevAPI'
    instrument = StringProperty(unique_index=True, required=True)
    model = StringProperty(unique_index=True, required=True)


class Researcher(UniqueNode):
    class Meta:
        app_label = 'Mat2DevAPI'
    name = StringProperty(unique_index=True, required=True)
    Facility = StringProperty(unique_index=True, required=True)
