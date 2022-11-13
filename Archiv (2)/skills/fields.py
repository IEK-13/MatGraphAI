from django.forms import URLField, model_to_dict, BaseFormSet

from dal import autocomplete
from django import forms
from django.urls import re_path as url
from neomodel import db

from graphutils.forms import RelationMultipleChoiceField, AutocompleteSingleChoiceField
from graphutils.views import AutocompleteView
from skills.models.education import Subject
from skills.models.ontology import OntologyOccupation



from skills.models.skills import Skill, ESCOSkill


class ESCOChoiceField(URLField):

    def __init__(self, autocomplete_url='esco-skill-autocomplete', **kwargs):
        super().__init__(**kwargs)
        self.widget = autocomplete.Select2(url=autocomplete_url)
        self.required = False

    def prepare_value(self, value):

        # make sure selected value is in choices to have it displayed right away
        if value and len(value):
            self.widget.choices = [
                (value, ESCOSkill.nodes.get(concept_url=value).full_label)
            ]

        return value


class SkillForm(forms.Form):

    single_parent = ESCOChoiceField()
    uid = forms.CharField(
        widget=forms.HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)

        if self.instance:
            data = model_to_dict(self.instance)

            if parent := self.instance.single_parent:
                data['single_parent'] = parent.concept_url

            kwargs['initial'] = data

        super().__init__(*args, **kwargs)

    # commit is ignored here
    def save(self, commit=False):

        #self.instance.label = self.cleaned_data['label']
        parent = ESCOSkill.nodes.get(concept_url=self.cleaned_data['single_parent']) if self.cleaned_data['single_parent'] else None

        # we only want skill groups. use skills group if a leaf is selected
        if parent and not parent.narrower.single():
            parent = parent.broader.single()

        self.instance.single_parent = parent
        return self.instance.save()

    def save_m2m(self):
        return

class InlineSkillForm(forms.Form):

    class _meta:
        labels = {}
        help_texts = {}
        model = Skill

    uid = forms.CharField(
        widget=forms.HiddenInput()
    )
    label = forms.CharField()
    priority = forms.ChoiceField(
        choices=(
            (0, "0 - Nicht Relevant"),
            (1, "1 - Kaum Relevant"),
            (2, "2 - Wenig Relevant"),
            (3, "3 - Etwas Relevant"),
            (4, "4 - Relevant"),
            (5, "5 - Sehr Relevant"),
            (6, "6 - Hoch Relevant"),
            (7, "7 - Extrem Relevant"),
        )
    )

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        self.parent = kwargs.pop('parent', None)

        if self.instance:
            data = model_to_dict(self.instance)
            if self.parent:
                data['priority'] = self.parent.skills.relationship(self.instance).priority
            else:
                data['priority'] = 1
            kwargs['initial'] = data

        super().__init__(*args, **kwargs)

        self.fields['label'].widget.attrs['readonly'] = True



class OccupationSkillsInlineNodeFormset(BaseFormSet):

    query = '''
            MATCH (occ)<-[rel:RELEVANT_FOR]-(skill:Skill)
            WHERE id(occ)=$self
            RETURN skill
            ORDER BY rel.priority DESC
        '''

    def __init__(self, *args, **kwargs):

        self.parent = kwargs.pop('instance')
        kwargs.pop('queryset')

        results, columns = self.parent.cypher(self.query)
        self.queryset = [Skill.inflate(row[0]) for row in results]

        self.nodes = list(self.queryset)

        kwargs.pop('save_as_new', "NONE")

        super().__init__(*args, **kwargs)

    def get_queryset(self):
        return self.queryset

    def initial_form_count(self):
        return len(self.nodes)

    def total_form_count(self):
        return self.initial_form_count()

    def _construct_form(self, i, **kwargs):
        kwargs['instance'] = self.nodes[i]
        kwargs['parent'] = self.parent
        return super()._construct_form(i, **kwargs)

    def save(self):

        self.new_objects = []
        self.changed_objects = []
        self.deleted_objects = []

        for index, skill in enumerate(self.get_queryset()):
            rel = self.parent.skills.relationship(skill)
            rel.priority = self.cleaned_data[index]['priority']
            rel.save()
            self.changed_objects.append((skill, self.cleaned_data[index]))


class CourseSkillsInlineNodeFormset(OccupationSkillsInlineNodeFormset):

    query = '''
            MATCH (course)-[rel:TEACHES]->(skill:Skill)
            WHERE id(course)=$self
            RETURN skill
            ORDER BY rel.priority DESC
        '''



class QuotaChoiceField(forms.ChoiceField):

    CHOICES = [
        (10, '10%'),
        (20, '20%'),
        (30, '30%'),
        (40, '40%'),
        (50, '50%'),
        (60, '60%'),
        (70, '70%'),
        (80, '80%'),
        (90, '90%'),
        (100, '100%'),
    ]

    def __init__(self, *args, **kwargs):
        kwargs['choices']=self.CHOICES
        super().__init__(*args, **kwargs)



class SkillMultipleChoiceField(RelationMultipleChoiceField):

    def __init__(self, autocomplete_url='skill-autocomplete', **kwargs):
        super().__init__('Skill', 'Skills', **kwargs)
        self.widget = autocomplete.Select2Multiple(url=autocomplete_url, attrs={'style': 'width: 100%;'})

    def prepare_value(self, value):

        # make sure selected value is in choices to have it displayed right away
        if value and len(value):
            self.widget.choices, meta = db.cypher_query(
                'MATCH (skill:Skill) WHERE skill.uid IN $uids RETURN skill.uid, skill.label',
                {'uids': value}
            )

        return value


class OccupationChoiceField(AutocompleteSingleChoiceField):

    model = OntologyOccupation
    autocomplete_url = 'occupation-autocomplete'


class SubjectChoiceField(AutocompleteSingleChoiceField):

    model = Subject
    autocomplete_url = 'subject-autocomplete'


class SkillAutocompleteView(AutocompleteView):

    model = Skill


class OccupationAutocompleteView(AutocompleteView):

    model = OntologyOccupation


class SubjectAutocompleteView(AutocompleteView):

    model = Subject


urlpatterns = [
    url(
        r'^autocomplete/skill/$',
        SkillAutocompleteView.as_view(),
        name='skill-autocomplete',
    ),
    url(
        r'^autocomplete/occupation/$',
        OccupationAutocompleteView.as_view(),
        name='occupation-autocomplete',
    ),
    url(
        r'^autocomplete/subject/$',
        SubjectAutocompleteView.as_view(),
        name='subject-autocomplete',
    )
]
