from django.contrib import admin as dj_admin
from django.contrib.admin import SimpleListFilter

from Mat2DevAPI.admins.adminBase import (NodeModelAdmin)
from Mat2DevAPI.choices.ChoiceFields import COMPONENT_TYPE_CHOICES
from Mat2DevAPI.forms.adminForms import ComponentAdminForm, MoleculeAdminForm, MaterialAdminForm
from Mat2DevAPI.models.matter import (Element,
                                      Molecule,
                                      Component,
                                      Device, Material)


class TypeFilter(SimpleListFilter):
    title = "Typ"
    parameter_name = "type"

    def lookups(self, request, model_admin):
        return COMPONENT_TYPE_CHOICES.items()

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(type=self.value())
        return queryset


@dj_admin.register(Component)
class ComponentAdmin(NodeModelAdmin):
    form = ComponentAdminForm
    list_display = ("uid",)
    list_filter = [TypeFilter]

    def save(self, commit=True):
        instance = super().save(commit)
        instance.user_skill = True
        instance.save()

        return instance

        def clean(self):
            cleaned_data = super().clean()

        return cleaned_data


@dj_admin.register(Element)
class ElementAdmin(dj_admin.ModelAdmin):
    class Meta:
        pass

    list_display = ("name", "abbreviation")


@dj_admin.register(Molecule)
class MoleculeAdmin(dj_admin.ModelAdmin):
    list_display = ("uid",
                    "SMILES",
                    "InChIKey",
                    "CAS",
                    "InChI",
                    "CompoundCID",
                    "IUPACName",
                    "sumFormula",
                    "AlternativeNames",
                    "nAtoms",
                    "molWeight",
                    "charge",
                    )
    form = MoleculeAdminForm

    def response_add(self, request, obj, post_url_continue=None):
        obj.pk = obj.uid  # make sure redirect after add works
        return super().response_add(request, obj, post_url_continue)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        if len(form.cleaned_data['elements']) == 0:
            form.instance.preselect_skills()

    def check(self, **kwargs):
        return []

    actions = ['delete_model']


@dj_admin.register(Material)
class MoleculeAdmin(dj_admin.ModelAdmin):
    # list_display = ("uid",
    #                 "SMILES",
    #                 "InChIKey",
    #                 "CAS",
    #                 "InChI",
    #                 "CompoundCID",
    #                 "IUPACName",
    #                 "sumFormula",
    #                 "AlternativeNames",
    #                 "nAtoms",
    #                 "molWeight",
    #                 "charge",
    #                 )
    form = MaterialAdminForm
    pass


@dj_admin.register(Device)
class DeviceAdmin(dj_admin.ModelAdmin):
    list_display = ("uid",)
