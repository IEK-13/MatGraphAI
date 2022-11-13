from Mat2DevAPI.views.baseViews import AutocompleteView
from Mat2DevAPI.models.matter import Element

class ElementAutocompleteView(AutocompleteView):
    model = Element
    autocomplete_url='element-autocomplete'
