from Mat2DevAPI.models.ontology import EMMO_Matter
from graphutils.forms import AutocompleteSingleChoiceField


class OntologyChoiceField(AutocompleteSingleChoiceField):
    model = EMMO_Matter
    autocomplete_url = 'emmomatter-autocomplete'