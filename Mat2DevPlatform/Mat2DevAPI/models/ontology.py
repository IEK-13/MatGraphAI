from Mat2DevAPI.models.abstractclasses import OntologyNode
from Mat2DevAPI.models.relationships import emmoIsA
from neomodel import RelationshipTo
from django.db import models


class EMMOMatter(OntologyNode):
    emmo_is_a = RelationshipTo("EMMO_Matter", "EMMO__IS_A", emmoIsA)
    pass


class EMMOQuantity(OntologyNode):
    emmo_is_a = RelationshipTo("EMMO_Quantity", "EMMO__IS_A", emmoIsA)
    pass


class EMMO_Process(OntologyNode):
    class Meta:
        verbose_name_plural = 'EMMO_Processes'
    app_label = 'Mat2DevAPI'
    # emmo_is_a = RelationshipTo(models.ForeignKey("EMMO_Process", on_delete=models.deletion.CASCADE), "EMMO__IS_A", emmoIsA)
    pass
