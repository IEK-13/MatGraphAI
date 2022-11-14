from django.contrib.admin.views.main import ChangeList
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import Select
from django import forms
from neomodel import db, RelationshipManager, StringProperty
from neomodel.match import QueryBuilder

from django.contrib.admin import ModelAdmin


class ChoiceWidgetBase:

    def __init__(self, *args, **kwargs):
        self.primary_key = kwargs.pop('primary_key', 'uid')
        self.node_label = kwargs.pop('node_label')
        self.label_field = kwargs.pop('label_field')
        super().__init__(*args, **kwargs)
        self.cached_choices = None

    @property
    def choices(self):
        if not self.cached_choices:
            self.cached_choices, meta = db.cypher_query(
                f'''
                    MATCH (n:{self.node_label})
                    RETURN n.{self.primary_key}, n.{self.label_field}
                    ORDER BY toLower(n.{self.label_field})
                '''
            )
        return self.cached_choices

    @choices.setter
    def choices(self, value):
        pass


class RelationMultipleChoiceWidget(ChoiceWidgetBase, FilteredSelectMultiple):
    pass


class RelationSingleChoiceWidget(ChoiceWidgetBase, Select):

    def __init__(self, *args, **kwargs):
        self.include_none_option = kwargs.pop('include_none_option', True)
        super().__init__(*args, **kwargs)

    @property
    def choices(self):
        if self.include_none_option:
            return [(None, '---')] + super().choices
        else:
            return super().choices

    @choices.setter
    def choices(self, value):
        pass


class RelationChoiceFieldBase:

    def __init__(self, widget, primary_key='uid', **kwargs):
        super().__init__(
            **kwargs
        )

        # it's important to set the widget after calling super().__init__
        # otherwise django tries to fetch choices before the db connection initializes
        self.widget = widget
        self.primary_key = primary_key

    # disable validation for now, as it's only relevant for internal backend
    # TODO: implement :)
    def validate(self, values):
        return

    # not the cleanest way to handle relation saving
    # done here, because primary_key is already known
    def save(self, relation_name, instance, data):
        rel = getattr(instance, relation_name)
        node_class = rel.definition['node_class']

        if isinstance(data, list):
            rel.disconnect_all()
            for value in data:
                if value:
                    rel.connect(
                        node_class.nodes.get(**{self.primary_key: value})
                    )
        elif data:

            # to avoid cardinality issues (One)
            try:
                old_node = rel.single()
            except BaseException:
                old_node = None
            finally:
                if old_node:
                    rel.reconnect(
                        old_node,
                        node_class.nodes.get(**{self.primary_key: data})
                    )
                else:
                    rel.connect(
                        node_class.nodes.get(**{self.primary_key: data})
                    )


class RelationMultipleChoiceField(RelationChoiceFieldBase, forms.MultipleChoiceField):

    def __init__(self, node_label, name_plural, primary_key='uid', label_field='label', **kwargs):
        super().__init__(
            widget=RelationMultipleChoiceWidget(name_plural, False, node_label=node_label, primary_key=primary_key,
                                                label_field=label_field),
            primary_key=primary_key,
            **kwargs
        )


class RelationSingleChoiceField(RelationChoiceFieldBase, forms.ChoiceField):

    def __init__(self, node_label, primary_key='uid', label_field='label', include_none_option=True, **kwargs):
        super().__init__(
            widget=RelationSingleChoiceWidget(node_label=node_label, primary_key=primary_key, label_field=label_field,
                                              include_none_option=include_none_option),
            primary_key=primary_key,
            **kwargs
        )





class NeoModelForm(forms.ModelForm):
    labels = {}

    def __init__(self, *args, **kwargs):

        if instance := kwargs.get('instance', None):

            kwargs['initial'] = {}

            for name, field in self.declared_fields.items():
                if isinstance(field, RelationMultipleChoiceField):
                    kwargs['initial'][name] = [
                        getattr(rel, field.primary_key)
                        for rel in getattr(instance, name).all()
                    ]
                elif isinstance(field, RelationSingleChoiceField):
                    try:
                        rel = getattr(instance, name).single()
                        kwargs['initial'][name] = getattr(rel, field.primary_key) if rel else None
                    except:
                        kwargs['initial'][name] = None

        super().__init__(*args, **kwargs)

        for field, label in self.labels.items():
            if field in self.fields:
                self.fields[field].label = label

    def save(self, commit=True):
        instance = super().save(commit)

        with db.transaction:
            instance.save()

            # save relations
            for changed in self.changed_data:
                if hasattr(instance, changed):
                    if isinstance(getattr(instance, changed), RelationshipManager):
                        self.fields[changed].save(changed, instance, self.cleaned_data[changed])

        return instance


class LocaleOrderingQueryBuilder(QueryBuilder):

    def build_order_by(self, ident, source):

        # cypher uses reversed ordering
        source._order_by.reverse()

        if '?' in source._order_by:
            super().build_order_by(ident, source)
        else:
            self._ast['order_by'] = []
            for p in source._order_by:
                field = p.split(' ')[0]
                if isinstance(getattr(source.model, field), StringProperty):
                    self._ast['order_by'].append(f'apoc.text.clean({ident}.{field}) {p.replace(field, "")}')
                else:
                    self._ast['order_by'].append(f'{ident}.{p}')


# fixes ordering
class NeoAdminChangelist(ChangeList):

    # only support ordering by one column to keep things simple by now
    def get_ordering(self, request, queryset):
        return super().get_ordering(request, queryset)[0:1]


class NodeModelAdmin(ModelAdmin):
    node_primary_key = 'uid'
    node_changelist_formset = None
    node_changelist_form = None

    # very important, unordered datasets save data in random places...
    ordering = ('uid',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs.query_cls = LocaleOrderingQueryBuilder
        return qs

    def get_changelist(self, request, **kwargs):
        return NeoAdminChangelist

    def get_changelist_formset(self, request, **kwargs):
        if self.node_changelist_form and self.node_changelist_formset:
            return forms.formset_factory(self.node_changelist_form, formset=self.node_changelist_formset)
        return super().get_changelist_formset(request, **kwargs)

    def save(self, commit):
        pass
