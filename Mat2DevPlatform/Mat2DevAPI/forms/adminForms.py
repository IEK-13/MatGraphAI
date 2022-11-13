from django import forms

from Mat2DevAPI.admins.adminBase import NeoModelForm
from Mat2DevAPI.choices.ChoiceFields import COMPONENT_TYPE_CHOICES, MATERIAL_STRUCTURE_CHOICEFIELD, \
    MATERIAL_MACROSTRUCTURE_CHOICEFIELD, MATERIAL_NANOSTRUCTURE_CHOICEFIELD, MATERIAL_MICROSTRUCTURE_CHOICEFIELD, \
    MATERIAL_LABEL_CHOICEFIELD
from Mat2DevAPI.fields.adminFields import ElementsMultipleChoiceField, RelationMultipleChoiceField


class ComponentAdminForm(forms.ModelForm):
    type = forms.ChoiceField(
        choices=COMPONENT_TYPE_CHOICES.items()
    )
    name = forms.CharField(widget=forms.Textarea, required=False)
    labels = {'type': 'Type',
              'name': 'Name'}
class MaterialAdminForm(forms.ModelForm):
    structure = forms.ChoiceField(
        choices=MATERIAL_STRUCTURE_CHOICEFIELD.items()
    )
    nanostructure = forms.ChoiceField(
        choices=MATERIAL_NANOSTRUCTURE_CHOICEFIELD.items()
    )
    microstructure = forms.ChoiceField(
        choices=MATERIAL_MICROSTRUCTURE_CHOICEFIELD.items()
    )
    macrostructure = forms.ChoiceField(
        choices=MATERIAL_MACROSTRUCTURE_CHOICEFIELD.items()
    )
    additional_label= forms.ChoiceField(
        choices=MATERIAL_LABEL_CHOICEFIELD.items()
    )
    # name = forms.CharField(widget=forms.Textarea, required=False)
    # labels = {'type': 'Type',
    #           'name': 'Name'}

class MoleculeAdminForm(NeoModelForm):
    elements = ElementsMultipleChoiceField()
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    # elements = RelationMultipleChoiceField('Element', 'Elements', primary_key='name')
class DateInput(forms.DateInput):
    input_type = 'date'
