import csv
import codecs
import django.db.models
from django.template.loader import render_to_string
from django.urls import path
from django.shortcuts import redirect, render
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django import forms
from django.forms import formset_factory
from django.utils.html import format_html
from nonrelated_inlines.admin import NonrelatedStackedInline

from graphutils.forms import RelationSingleChoiceField, NeoModelForm
from skills.fields import RelationMultipleChoiceField, QuotaChoiceField, \
    SkillMultipleChoiceField, OccupationChoiceField, SubjectChoiceField
from .importer import import_wp_csv
from skills.models.education import Subject
from jobs.models import MatchedCandidate
from skills.models.ontology import OntologyOccupation
from workprofiles.models import WORKPROFILE_TYPE_CHOICES, ExternalWorkProfile
from neomodel import db, Q


class TypeFilter(SimpleListFilter):

    title = "Typ"
    parameter_name = "type"

    def lookups(self, request, model_admin):
        return WORKPROFILE_TYPE_CHOICES.items()

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(type=self.value())
        return queryset


class ClaimedFilter(SimpleListFilter):

    title = "Claimed"
    parameter_name = "claimed"

    def lookups(self, request, model_admin):
        return (
            (1, 'Claimed'),
            (0, 'Not Claimed')
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(claimed=False)
        elif self.value() == '1':
            return queryset.filter(claimed=True)
        return queryset


class ImportedUncheckedFilter(SimpleListFilter):

    title = "Importiert & nicht gerpüft"
    parameter_name = "imported_unchecked"

    def lookups(self, request, model_admin):
        return (
            (0, 'Bereits geprüft'),
            (1, 'Noch nicht geprüft'),
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(imported_unchecked=False)
        elif self.value() == '1':
            return queryset.filter(imported_unchecked=True)
        return queryset

class DateInput(forms.DateInput):
    input_type = 'date'


class CVRelForm(forms.BaseForm):

    base_fields = {
        'id': forms.IntegerField(widget=forms.HiddenInput, required=False),
        'since': forms.DateField(widget=DateInput, label="Von", required=False),
        'until': forms.DateField(widget=DateInput, label="Bis", required=False),
        'title': forms.CharField(label="Titel", required=False)
    }

    class Meta:
        fields = []
    class _meta:
        labels = None
        exclude = []
        fields = []
        help_texts = []
        model = MatchedCandidate

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)


class CVRelFormset(forms.BaseFormSet):

    _pk_field = django.db.models.CharField(name="id")

    def __init__(self, *args, **kwargs):

        kwargs.pop('queryset')
        kwargs.pop('save_as_new', None)

        self.instance = kwargs.pop('instance')
        self.initial = self.get_initial()
        kwargs['initial'] = self.initial

        super().__init__(*args, **kwargs)

    def get_queryset(self):
        return self.initial

    @db.read_transaction
    def get_initial(self):
        if not hasattr(self.instance, "id"):
            return {}
        return self.load(self.instance)

    def load(self, instance):
        raise NotImplementedError()

    def save(self, *args, **kwargs):

        rel = getattr(self.instance, self.attribute_name)

        # TODO: consolidate into single query for performance
        with db.write_transaction:
            rel.disconnect_all()
            for item in self.cleaned_data:
                if not item.pop('DELETE', False):
                    item.pop('id')

                    node = self.target_class.nodes.get(uid=item.pop(self.target_field))

                    # make sure empty values are not saved as empty strings
                    for key, value in item.items():
                        if value == '':
                            item[key] = None

                    if not item['title']:
                        item['title'] = node.label

                    rel.connect(node, item)

        # only used for change messages and therefore not important
        self.new_objects = []
        self.changed_objects = []
        self.deleted_objects = []


class CVRelTabularInline(NonrelatedStackedInline):

    # display no empty rows by default
    extra = 0

    # force tabular inline template (library only has NonrelatedStackedInline)
    template = 'admin/edit_inline/tabular.html'

    class Media:
        css = {
            'all': ('css/hide-object-name.css',) # hide object name in CV rows
        }

    # some random model to keep admin checks happy
    model = MatchedCandidate
    def get_form_queryset(self, obj):
        return MatchedCandidate.objects.none()


class EducationForm(CVRelForm):

    base_fields = {
        **CVRelForm.base_fields,
        'subject': SubjectChoiceField(include_none_option=False, label="Studienrichtung"),
        'degree': RelationSingleChoiceField('Degree', include_none_option=True, label="Abschluss"),
        'school': RelationSingleChoiceField('School', include_none_option=True, label="Hochschule")
    }


class EducationFormsetCls(CVRelFormset):

    attribute_name = 'educations'
    target_field = 'subject'
    target_class = Subject

    def load(self, instance):

        result, meta = instance.cypher('''
            MATCH (wp:WorkProfile)-[rel:STUDIED]->(subject:Subject)
            WHERE ID(wp)=$self
            RETURN
                ID(rel) as rel,
                subject.uid as subject,
                rel.since as since, rel.until as until,
                rel.title as title, rel.degree as degree,
                rel.school as school
        ''')

        return [
            {
                'id': sub[0], 'subject': sub[1], 'since': sub[2], 'until': sub[3],
                'title': sub[4], 'degree': sub[5], 'school': sub[6]
            }
            for sub in result
        ]


class TabularEducationInline(CVRelTabularInline):

    form = EducationForm
    formset = formset_factory(EducationForm, formset=EducationFormsetCls)

    verbose_name = "Ausbildung"
    verbose_name_plural = "Ausbildungen"


class OccupationForm(CVRelForm):

    base_fields = {
        **CVRelForm.base_fields,
        'occupation': OccupationChoiceField(include_none_option=False, label="Beruf"),
        'company': forms.CharField(label="Unternehmen", required=False),
        'description': forms.CharField(label="Beschreibung", required=False)
    }


class OccupationFormsetCls(CVRelFormset):

    attribute_name = 'occupations'
    target_field = 'occupation'
    target_class = OntologyOccupation

    def load(self, instance):

        result, meta = instance.cypher('''
            MATCH (wp:WorkProfile)-[rel:WORKED_AS]->(occ:OntologyOccupation)
            WHERE ID(wp)=$self
            RETURN
                ID(rel) as rel,
                occ.uid as occupation,
                rel.since as since, rel.until as until,
                rel.title as title, rel.company as company,
                rel.description as description
        ''')

        return [
            {
                'id': occ[0], 'occupation': occ[1], 'since': occ[2], 'until': occ[3],
                'title': occ[4], 'company': occ[5], 'description': occ[6]
            }
            for occ in result
        ]


class TabularOccupationInline(CVRelTabularInline):

    form = OccupationForm
    formset = formset_factory(OccupationForm, formset=OccupationFormsetCls)

    verbose_name = "Beruf"
    verbose_name_plural = "Berufe"


class WorkProfileAdminForm(NeoModelForm):

    min_quota = QuotaChoiceField(initial=10)
    max_quota = QuotaChoiceField(initial=100)

    skills = SkillMultipleChoiceField()
    personality_types = RelationMultipleChoiceField('PersonalityType', 'Persönlichkeitstypen', primary_key='code')
    cantons = RelationMultipleChoiceField('Canton', 'Kantone', primary_key='code')
    job_categories = RelationMultipleChoiceField('JobCategory', 'Job-Kategorien')
    #company_sizes = RelationMultipleChoiceField('CompanySize', 'Unternehmensgrössen')
    notes = forms.CharField(widget=forms.Textarea, required=False)
    interests = forms.CharField(widget=forms.Textarea, required=False)
    about_me = forms.CharField(widget=forms.Textarea, required=False)

    type = forms.ChoiceField(
        choices=[('external', 'External Workprofile')],
        initial='external'
    )

    labels = {
        'open_for_remote_work': "Offen für Remote-Arbeit",
        'min_quota': "Minimales Pensum*",
        'max_quota': "Maximales Pensum*",
        'first_name': 'Vorname*',
        'last_name': 'Nachname*',
        'email': "E-Mail Adresse",
        'phone_number': "Telefon",
        'personality_types': 'Persönlichkeitstypen*',
        'cantons': 'Kantone',
        'job_categories': 'Job-Kategorien',
        #'company_sizes': 'Unternehmensgrössen',
        'notes': 'Notizen',
        'interests': 'Interessen',
        'about_me': "Über mich",
        'claimed': 'Nutzer registriert',
        'imported_unchecked': 'Zu prüfen (Importiert)',
        'profile_url': "Profil-Link"
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def clean(self):
        cleaned_data = super().clean()

        if int(cleaned_data['min_quota']) > int(cleaned_data['max_quota']):
            raise forms.ValidationError("Quota values not correct")

        return cleaned_data

class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


@admin.register(ExternalWorkProfile)
class WorkProfileAdmin(admin.ModelAdmin):

    class Meta:
        pass

    list_display = [
        'name',
        'email',
        'created',
        'get_claimed',
        'uid',
        'import_identifier',
        'get_claim_link'
    ]

    search_fields = ('title', ) # only set to enable search. Actual search is handled by get_search_results()

    change_list_template = "workprofiles_changelist.html"
    fields = (
        ('uid', 'created'),
        ('type', 'get_claimed', 'import_identifier'),
        ('min_quota', 'max_quota', 'open_for_remote_work'),
        ('first_name', 'last_name'),
        ('phone_number', 'email', 'profile_url'),
        ('notes', 'interests', 'about_me'),
        'personality_types',
        'job_categories',
        'get_imported_data',
        'cantons',
        #'company_sizes',
        'skills',
        'imported_unchecked',
        'get_interests'
    )

    list_filter = [
        ClaimedFilter,
        ImportedUncheckedFilter
    ]

    readonly_fields = [
        'uid',
        'created',
        'type',
        'get_claimed',
        'get_imported_data',
        'get_interests'
    ]

    inlines = [TabularOccupationInline, TabularEducationInline]

    def get_search_results(self, request, queryset, search_term):

        if search_term:
            queryset = queryset.filter(
                Q(email__icontains=search_term) |
                Q(first_name__icontains=search_term) |
                Q(last_name__icontains=search_term) |
                Q(uid=search_term)
            )
        may_have_duplicates = False

        return queryset, may_have_duplicates

    def get_imported_data(self, profile):
        notes = str(profile.imported_data).replace('{','').replace('}','').replace(',','\n').replace("'","")
        return notes

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            reader = csv.DictReader(codecs.iterdecode(csv_file, 'utf-8'), delimiter=';')

            import_wp_csv(reader, self.message_user, request)

            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "admin/csv_form.html", payload
        )

    form = WorkProfileAdminForm

    # to allow hacked inlines
    def check(self, **kwargs):
        return []

    def get_interests(self, obj):
        return render_to_string(
            'admin/interest_table_jobs.html',
            {
                'interests': sorted([
                    (job, obj.interested_in_jobs.relationship(job))
                    for job in obj.interested_in_jobs.all()
                ], key=lambda rel: rel[1].when)
            }
        )
    get_interests.short_description = "Job-Bewerbungen"

    def get_claimed(self, profile):
        return format_html(f"<a href='{profile.claim_link}' target='_blank'>Link{' (Claimed)' if profile.claimed else ''}</a>", url=profile.claim_link)
    get_claimed.short_description = "Claim"

    def get_claim_link(self, profile):
        return profile.claim_link
    get_claim_link.short_description = "Claim-Link"

    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)

    def has_change_permission(self, request, obj=None):
        return obj and obj.type == 'external'

    #prevent checking the profile if the profile is not external type
    # def has_view_permission(self, request, obj=None):
    #     return self.has_change_permission(request, obj)

    def has_add_permission(self, request):
        return True

    def response_add(self, request, obj, post_url_continue=None):
        obj.pk = obj.uid # make sure redirect after add works
        return super().response_add(request, obj, post_url_continue)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        if len(form.cleaned_data['skills']) == 0:
            form.instance.preselect_skills()