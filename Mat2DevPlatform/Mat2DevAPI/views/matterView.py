from Mat2DevAPI.views.baseViews import AutocompleteView
from Mat2DevAPI.models.matter import Element, Material


class ElementAutocompleteView(AutocompleteView):
    model = Element
    autocomplete_url='element-autocomplete'

class MaterialInputAutocompleteView(AutocompleteView):
    model = Material
    autocomplete_url='material-input-autocomplete'