from Mat2DevAPI.choices.ChoiceFields import COMPONENT_TYPE_CHOICES
from django import forms

class ComponentTypeChoiceField(forms.ChoiceField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = COMPONENT_TYPE_CHOICES.items()
        super().__init__(*args, **kwargs)