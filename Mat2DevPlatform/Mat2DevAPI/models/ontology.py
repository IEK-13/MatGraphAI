from neomodel import RelationshipTo

from Mat2DevAPI.models.abstractclasses import OntologyNode
from Mat2DevAPI.models.relationships import emmoIsA


class EMMOQuantity(OntologyNode):
    emmo_is_a = RelationshipTo("EMMO_Quantity", "EMMO__IS_A", emmoIsA)
    pass


class EMMO_Matter(OntologyNode):
    class Meta:
        verbose_name_plural = 'EMMO Matter'

    app_label = 'Mat2DevAPI'
    # emmo_is_a = RelationshipTo(models.ForeignKey("EMMO_Process", on_delete=models.deletion.CASCADE), "EMMO__IS_A",
    # emmoIsA)
    pass


class EMMO_Process(OntologyNode):
    class Meta:
        verbose_name_plural = 'EMMO Processes'
    app_label = 'Mat2DevAPI'
    pass
