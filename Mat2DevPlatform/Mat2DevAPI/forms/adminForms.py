from django import forms

from Mat2DevAPI.admins.adminBase import NeoModelForm

from Mat2DevAPI.fields.adminFields import RegularTypeChoiceField, RelationMultipleChoiceField, ElementsMultipleChoiceField

from Mat2DevAPI.choices.ChoiceFields import INSTITUTION_TYPE_CHOICEFIELD


# class ComponentAdminForm(forms.ModelForm):
#     type = forms.ChoiceField(
#         choices=COMPONENT_TYPE_CHOICES.items()
#     )
#     name = forms.CharField(widget=forms.Textarea, required=False)
#     labels = {'type': 'Type',
#               'name': 'Name'}
# class MaterialAdminForm(forms.ModelForm):
#     structure = forms.ChoiceField(
#         choices=MATERIAL_STRUCTURE_CHOICEFIELD.items()
#     )
#     nanostructure = forms.ChoiceField(
#         choices=MATERIAL_NANOSTRUCTURE_CHOICEFIELD.items()
#     )
#     microstructure = forms.ChoiceField(
#         choices=MATERIAL_MICROSTRUCTURE_CHOICEFIELD.items()
#     )
#     macrostructure = forms.ChoiceField(
#         choices=MATERIAL_MACROSTRUCTURE_CHOICEFIELD.items()
#     )
#     additional_label= forms.ChoiceField(
#         choices=MATERIAL_LABEL_CHOICEFIELD.items()
#     )
#     # name = forms.CharField(widget=forms.Textarea, required=False)
#     # labels = {'type': 'Type',
#     #           'name': 'Name'}
#
class MoleculeAdminForm(NeoModelForm):
    elements = ElementsMultipleChoiceField()
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    elements = RelationMultipleChoiceField('Element', 'Elements', primary_key='name')


class DateInput(forms.DateInput):
    input_type = 'date'

class ManufacturingAdminForm(NeoModelForm):

    material_input = RelationMultipleChoiceField("Material", "Materials", primary_key = "uid", label_field='name')
    material_output = RelationMultipleChoiceField("Material", "Materials", primary_key = "uid", label_field='name')
    is_a = RelationMultipleChoiceField("EMMOProcess", "EMMO Processes", primary_key = 'uid',label_field='EMMO__name')
    date_added =DateInput()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

class ResearcherAdminForm(NeoModelForm):

    country = RelationMultipleChoiceField("Country", "Countries", primary_key = "uid", label_field='name')
    institution = RelationMultipleChoiceField("Institution", "Institutions", primary_key = "uid", label_field='name')
    date_added =DateInput()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

class InstitutionAdminForm(NeoModelForm):
    type = RegularTypeChoiceField(INSTITUTION_TYPE_CHOICEFIELD)

    country = RelationMultipleChoiceField("Country", "Countries", primary_key = "uid", label_field='name')
    date_added = DateInput()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

class CsvImportForm(forms.Form):
    csv_file = forms.FileField()
