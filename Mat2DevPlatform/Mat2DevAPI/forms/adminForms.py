from django import forms

from Mat2DevAPI.choices.ChoiceFields import COMPONENT_TYPE_CHOICES


class ComponentAdminForm(forms.ModelForm):
    type = forms.ChoiceField(
        choices=COMPONENT_TYPE_CHOICES.items()
    )
