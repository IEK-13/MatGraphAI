from neomodel import RelationshipTo, RelationshipFrom
from Mat2DevAPI.models.abstractclasses import CausalObject


class PhysicalDimension(CausalObject):
    """
    Class representing a physical dimension in the knowledge graph.
    """
    class Meta:
        app_label = 'Mat2DevAPI'

    __abstract_node__ = True


class Property(PhysicalDimension):
    """
    Class representing a property in the knowledge graph.
    """
    class Meta:
        verbose_name_plural = 'properties'
        app_label = 'Mat2DevAPI'

    derived_property = RelationshipTo('Property', "derivedFrom")
    property = RelationshipFrom('Mat2DevAPI.models.processes.Measurement', "YIELDS_PROPERTY")

    pass


class Parameter(PhysicalDimension):
    """
    Class representing a parameter in the knowledge graph.
    """
    parameter = RelationshipFrom('Mat2DevAPI.models.processes.Process', "HAS_PARAMETER")

    pass
