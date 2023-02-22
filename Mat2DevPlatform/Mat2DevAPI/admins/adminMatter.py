"""All admin classes that are required for "matter" models. Contains Typefilters, to allow filtering of "matter"
classes by certain properties and the model admins. AdminClasses register the models on the admin site and allow
reading writing and deleting of their instances via the admin interface """

from django.contrib import admin as dj_admin
from django.contrib.admin import SimpleListFilter

from Mat2DevAPI.admins.adminBase import (NodeModelAdmin)
from Mat2DevAPI.choices.ChoiceFields import COMPONENT_TYPE_CHOICES
# from Mat2DevAPI.forms.adminForms import ComponentAdminForm, MoleculeAdminForm, MaterialAdminForm
from Mat2DevAPI.models.matter import (Element,
                                      Molecule,
                                      Component,
                                      Device, Material)


# Allows filtering by type
class TypeFilter(SimpleListFilter):
    title = "Typ"
    parameter_name = "type"

    # List of type choices
    def lookups(self, request, model_admin):
        return COMPONENT_TYPE_CHOICES.items()

    # Returns queryset and allows filtering by value, which is a string
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(type=self.value())
        return queryset


# ComponentAdmin represents the component class in the admin site.
@dj_admin.register(Component)
class ComponentAdmin(NodeModelAdmin):
    # ComponentAdmin form is necessary for the dropdown menu to choose the Component type
    # form = ComponentAdminForm
    # list_display determines which properties are displayed
    list_display = ["uid"]

    # Allows Filtering for types
    list_filter = [TypeFilter]

    # save function, necessary to save instances
    def save(self, commit=True):
        instance = super().save(commit)
        instance.user_skill = True
        instance.save()

        return instance

# ElementAdmin represents the element class in the admin site.
@dj_admin.register(Element)
class ElementAdmin(NodeModelAdmin):
    class Meta:
        pass
    # displays the "name" and "abbreviation" on the admin site
    list_display = ("name",
                    "symbol")


@dj_admin.register(Molecule)
class MoleculeAdmin(NodeModelAdmin):
    list_display = ("uid",
                    "SMILES",
                    "InChI_key",
                    "CAS",
                    "InChI",
                    "compound_cid",
                    "IUPAC_name",
                    "chemical_formula",
                    )
    # form = MoleculeAdminForm

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
class MaterialAdmin(dj_admin.ModelAdmin):
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
    # form = MaterialAdminForm
    pass


@dj_admin.register(Device)
class DeviceAdmin(dj_admin.ModelAdmin):
    list_display = ("uid",
                    "name")
