from django_neomodel import DjangoNode
from neomodel import RelationshipTo, RelationshipFrom, ArrayProperty, FloatProperty, One

from Mat2DevAPI.models.abstractclasses import OntologyNode
from Mat2DevAPI.models.relationships import IsARel


class EMMOQuantity(OntologyNode):
    """
    Class representing EMMO quantity in the knowledge graph.
    """
    emmo_is_a = RelationshipTo("EMMO_Quantity", "EMMO__IS_A", model=IsARel)
    pass


class EMMO_Matter(OntologyNode):
    """
    Class representing EMMO matter in the knowledge graph.
    """
    class Meta:
        verbose_name_plural = 'EMMO Matter'

    app_label = 'Mat2DevAPI'

    is_a = RelationshipFrom('Mat2DevAPI.models.matter.Matter', "IS_A", model=IsARel)

    pass


class EMMO_Process(OntologyNode):
    """
    Class representing EMMO process in the knowledge graph.
    """
    class Meta:
        verbose_name_plural = 'EMMO Processes'
    app_label = 'Mat2DevAPI'

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
