from django_neomodel import DjangoNode, classproperty
from neomodel import RelationshipTo, RelationshipFrom, ArrayProperty, FloatProperty, One, OneOrMore, ZeroOrMore, \
    StringProperty, UniqueIdProperty, AliasProperty

from django import apps
from Mat2DevAPI.models.abstractclasses import OntologyNode
from Mat2DevAPI.models.relationships import IsARel


class EMMOQuantity(OntologyNode):
    """
    Class representing EMMO quantity in the knowledge graph.
    """
    emmo_is_a = RelationshipTo("EMMOQuantity", "EMMO__IS_A", model=IsARel)
    emmo_subclass =RelationshipTo('Mat2DevAPI.models.ontology.EMMOQuantity', 'EMMO__IS_A', cardinality=ZeroOrMore)

    pass


class EMMOMatter(OntologyNode):
    """
    Class representing EMMO matter in the knowledge graph.
    """
    class Meta:
        verbose_name_plural = 'EMMO Matter'

    app_label = 'Mat2DevAPI'

    is_a = RelationshipFrom('Mat2DevAPI.models.matter.Matter', "IS_A", model=IsARel, cardinality=ZeroOrMore)
    emmo_subclass =RelationshipTo('Mat2DevAPI.models.ontology.EMMOMatter', 'EMMO__IS_A', cardinality=ZeroOrMore)

    pass


class EMMOProcess(OntologyNode):
    """
    Class representing EMMO process in the knowledge graph.
    """
    class Meta:
        verbose_name_plural = 'EMMO Processes'
    app_label = 'Mat2DevAPI'
    emmo_subclass =RelationshipTo('Mat2DevAPI.models.ontology.EMMOProcess', 'EMMO__IS_A', cardinality=ZeroOrMore)

    is_a = RelationshipFrom('Mat2DevAPI.models.processes.Process', "IS_A", model=IsARel)

    pass


class ModelEmbedding(DjangoNode):

    class Meta:
        app_label = "Mat2DevAPI"

    element = RelationshipFrom('graphutils.models.AlternativeLabel', 'HAS_LABEL', One)
    vector = ArrayProperty(
        base_property=FloatProperty(),
        required=True
    )
