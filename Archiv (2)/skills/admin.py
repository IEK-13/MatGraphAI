from django.contrib import admin
from django.contrib.admin import ModelAdmin, SimpleListFilter, TabularInline
from django import forms
from django.contrib.admin.checks import ModelAdminChecks, InlineModelAdminChecks
from django_neomodel import NeoNodeSet
from neomodel import Q

from graphutils.admin import NodeModelAdmin, ChangelistNodeFormset
from graphutils.forms import NeoModelForm, RelationMultipleChoiceField, RelationSingleChoiceField
from x28_ontology.models import SCODirectory, SCO

from skills.fields import SkillForm, InlineSkillForm, \
    OccupationSkillsInlineNodeFormset, CourseSkillsInlineNodeFormset
from .models.admin import JobField
from .models.education import Course
from .models.skills import SKILL_TYPE_CHOICES, Skill, ESCOSkill, OntologyOccupation, BaseSkill


class ESCOConnectionFilter(SimpleListFilter):

    title = "ESCO-Zuordnung"
    parameter_name = "esco-relation"

    def lookups(self, request, model_admin):
        return (
            ('existing', 'Zuordnung vorhanden'),
            ('missing', 'Keine Zuordnung vorhanden')
        )

    def queryset(self, request, queryset):
        if self.value() == 'missing':
            return queryset.has(broader=False)
        elif self.value() == 'existing':
            return queryset.has(broader=True)
        return queryset

class OccupationFilter(SimpleListFilter):

    title = "Job"
    parameter_name = 'job'

    def lookups(self, request, model_admin):
        return [(occ.uid, occ.label) for occ in OntologyOccupation.nodes.order_by('label')]

    def queryset(self, request, queryset):
        if self.value():

            # TODO: should not be needed since BaseNode overwrites nodes() to use NeoNodeSet
            # super hacky
            # OntologyOccupation.skills is NodeSet instead of NeoNodeSet
            # and queryset can not be filtered for a relationship to a specific node
            traversal = OntologyOccupation._default_manager.get_queryset().skills
            traversal.source = OntologyOccupation.nodes.get(uid=self.value())
            return NeoNodeSet(source=traversal)

        return queryset

class LabelFilter(SimpleListFilter):

    title = "Label vorhanden"
    parameter_name = "label"

    def lookups(self, request, model_admin):
        return (
            ('yes', "Label vorhanden"),
            ('no', "Kein Label vorhanden oder automatisch generiert")
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.exclude(label="").exclude(label__endswith="[AUTO]")
        elif self.value() == 'no':
            return queryset.filter(Q(label="") | Q(label__endswith="[AUTO]"))
        return queryset


class JobClusterFilter(SimpleListFilter):

    title = "Job-Cluster"
    parameter_name = "job_cluster"

    def lookups(self, request, model_admin):
        return [
            (cluster.id, cluster.name) for cluster in
            SCODirectory.objects.get(name="x28 AG").scos.order_by('name')
        ]

    def queryset(self, request, queryset):

        if self.value():

            query = Q()
            sco = SCO.objects.get(id=self.value())
            for occ in sco.occupations.all():
                query |= Q(label=occ.name)

            qs = OntologyOccupation.nodes.filter(query).skills
            return NeoNodeSet(qs)

        return queryset


class JobClusterOccupationFilter(SimpleListFilter):

    title = "Job-Cluster"
    parameter_name = "job_cluster"

    def lookups(self, request, model_admin):
        return [
            (cluster.id, cluster.name) for cluster in
            SCODirectory.objects.get(name="x28 AG").scos.order_by('name')
        ]

    def queryset(self, request, queryset):

        if self.value():

            query = Q()
            sco = SCO.objects.get(id=self.value())
            for occ in sco.occupations.all():
                query |= Q(label=occ.name)

            return queryset.filter(query)

        return queryset


class JobFieldFilter(SimpleListFilter):

    title = "Job-Field"
    parameter_name = "job_field"

    def lookups(self, request, model_admin):
        return [(field.pk, field.name) for field in JobField.objects.all()]

    def queryset(self, request, queryset):

        if self.value():

            query = Q()
            field = JobField.objects.get(pk=self.value())

            for cluster in field.clusters.all():
                cluster = SCO.objects.get(pk=cluster.sco_id)
                for occ in cluster.occupations.all():
                    query |= Q(label=occ.name)

            qs = OntologyOccupation.nodes.filter(query).skills
            return NeoNodeSet(qs)

        return queryset

class AddedSkillFilter(SimpleListFilter):
    
    title = "User Added Skill"
    parameter_name = "user_skill"

    def lookups(self, request, model_admin):
        return (
            ('1', "Is User Skill"),
            ('0', "Is Scrambl. Skill")
        )
    
    def queryset(self, request, queryset):

        if self.value() == '0':
            return queryset.filter(user_skill=False)
        elif self.value() == '1':
            return queryset.filter(user_skill=True)
        else:
            return queryset

class SkillTypeChoiceField(forms.ChoiceField):


    def __init__(self, *args, **kwargs):
        kwargs['choices']=SKILL_TYPE_CHOICES.items()
        super().__init__(*args, **kwargs)


class SkillAdminForm(NeoModelForm):

    labels = {
        'label': 'Label',
        'type': 'Typ',
        'occupations':'Occupation',
        'predicate':'Predicate',
        'personality_types':'Personality Types',
        'topics':'Topics'
    }

    type = SkillTypeChoiceField()
    occupations = RelationMultipleChoiceField('OntologyOccupation', name_plural='occupations')
    predicate = RelationSingleChoiceField('OntologyPredicate')
    personality_types = RelationMultipleChoiceField('PersonalityType', name_plural='personality types')
    topics = RelationSingleChoiceField('OntologyTopic')

    def save(self, commit=True):
        instance = super().save(commit)
        instance.user_skill=True
        instance.save()

        return instance


@admin.register(Skill)
class SkillAdmin(NodeModelAdmin):

    class Media:
        css = {
            'all': ('css/admin.css',)
        }

    node_changelist_formset = ChangelistNodeFormset
    node_changelist_form = SkillForm

    list_filter = (
        JobClusterFilter,
        JobFieldFilter,
        OccupationFilter,
        ESCOConnectionFilter,
        LabelFilter,
        AddedSkillFilter,
    )

    form = SkillAdminForm

    list_display = [
        'get_occupations',
        'label',
        'topic_label',
        'predicate_label',
        'single_parent',
        'get_parent_recommendation',
        'uid',
        'user_skill'
    ]

    readonly_fields = (
        'user_skill', 'uid'
    )

    # not really editable. just used to force django to render the form
    # TODO: find a better workaround
    list_editable = ('label',)

    def has_delete_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request):
        return True

    def topic_label(self, obj):
        return obj.single_topic.label if obj.single_topic else None

    def predicate_label(self, obj):
        return obj.predicate.single().label if obj.predicate.single() else None

    def get_occupations(self, obj):
        occupations = [occ.label for occ in obj.occupations.all()]
        occ = ', '.join(occupations[:4])
        if len(occupations) > 4:
            occ += ' & weitere'
        return occ
    get_occupations.short_description = "Occupations"

    # looks for other skills sharing the same topic and makes a BROADER_THAN recommendation
    def get_parent_recommendation(self, skill):

        results, columns = skill.cypher('''
                                        MATCH (other_skill:Skill)-[]->(:OntologyTopic)<-[]-(base_skill)
                                        MATCH (other_skill)<-[:BROADER_THAN]-(recommended_parent:BaseSkill)
                                        WHERE id(base_skill)=$self
                                        RETURN recommended_parent
                                        LIMIT 1
                                        ''')

        if len(results):
            return BaseSkill.inflate(results[0][0]).label

        return "-"
    get_parent_recommendation.short_description = "Proposal"


@admin.register(ESCOSkill)
class ESCOSkillAdmin(ModelAdmin):
    list_display = ['concept_url', 'label', 'get_parent']

    def get_parent(self, obj):
        if parent := obj.single_parent:
            return parent.label
        return None
    get_parent.short_description = "Parent"

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False




class SkillModelAdminChecks(ModelAdminChecks):

    # disable checks for inlines, as we do not use django models
    def _check_inlines_item(self, obj, inline, label):
        return []


class SkillInlineModelAdminChecks(InlineModelAdminChecks):
    """
    Check used by the admin system to determine whether or not an inline model
    has a relationship to the parent object.

    In this case we always want this check to pass.
    """
    def _check_exclude_of_parent_model(self, obj, parent_model):
        return []

    def _check_relation(self, obj, parent_model):
        return []


class OccupationSkillListTabularInline(TabularInline):

    class Media:
        css = {
            'all': ('css/wide_inputs.css',)
        }

    checks_class = SkillInlineModelAdminChecks

    extra = 0
    model = Skill
    fields = [
        'uid',
        'label',
        'priority',
    ]

    def get_formset(self, request, obj=None, **kwargs):
        return forms.formset_factory(InlineSkillForm, formset=OccupationSkillsInlineNodeFormset)


class CourseSkillListTabularInline(OccupationSkillListTabularInline):

    def get_formset(self, request, obj=None, **kwargs):
        return forms.formset_factory(InlineSkillForm, formset=CourseSkillsInlineNodeFormset)


@admin.register(OntologyOccupation)
class OccupationSkillListAdmin(ModelAdmin):

    checks_class = SkillModelAdminChecks

    list_display = ('ontology_id', 'label',)
    inlines = [OccupationSkillListTabularInline]
    list_filter = [JobClusterOccupationFilter]
    #readonly_fields = ('ontology_id', 'label',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True


@admin.register(Course)
class CourseSkillListAdmin(ModelAdmin):

    checks_class = SkillModelAdminChecks

    list_display = ('uid', 'get_subject', 'get_degree')
    inlines = [CourseSkillListTabularInline]

    def get_subject(self, obj):
        return obj.subject.single().label
    get_subject.short_description = "Studienrichtung"

    def get_degree(self, obj):
        return obj.degree.single().label
    get_degree.short_description = "Abschluss"

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True
