from Mat2DevAPI.choices.ChoiceFields import INSTITUTION_TYPE_CHOICEFIELD
from Mat2DevAPI.fields.adminFields import RegularTypeChoiceField
from graphutils.forms import NeoModelForm, RelationMultipleChoiceField, DateInput, RelationSingleChoiceField


class ResearcherAdminForm(NeoModelForm):

    country = RelationMultipleChoiceField("Country", "Countries", primary_key = "uid", label_field='name')
    institution = RelationMultipleChoiceField("Institution", "Institutions", primary_key = "uid", label_field='name')
    date_added =DateInput()

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

class InstitutionAdminForm(NeoModelForm):

    type = RegularTypeChoiceField(INSTITUTION_TYPE_CHOICEFIELD)
    country = RelationSingleChoiceField("Country", "Countries", label_field='name')
    date_added = DateInput()

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
