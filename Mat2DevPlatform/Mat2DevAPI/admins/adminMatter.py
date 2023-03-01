"""All admin classes that are required for "matter" models. Contains Typefilters, to allow filtering of "matter"
classes by certain properties and the model admins. AdminClasses register the models on the admin site and allow
reading writing and deleting of their instances via the admin interface """

from django.contrib import admin as dj_admin
from neomodel import Q

from Mat2DevAPI.admins.adminBase import (NodeModelAdmin)
from Mat2DevAPI.forms.formsMatter import MoleculeAdminForm, MaterialAdminForm, DeviceAdminForm
from Mat2DevAPI.models.matter import (Element,
                                      Molecule,
                                      Component,
                                      Device, Material)


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
    form = MoleculeAdminForm

    def response_add(self, request, obj, post_url_continue=None):
        obj.pk = obj.uid  # make sure redirect after add works
        return super().response_add(request, obj, post_url_continue)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

    def check(self, **kwargs):
        return []

    actions = ['delete_model']


@dj_admin.register(Material)
class MaterialAdmin(NodeModelAdmin):
    # inlines = [OntologyInline]
    form = MaterialAdminForm
    list_display = ("name", "uid")
    pass

    def check(self, **kwargs):
        return []

    def response_add(self, request, obj, post_url_continue=None):
        obj.pk = obj.uid  # make sure redirect after add works
        return super().response_add(request, obj, post_url_continue)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

    search_fields = ('name',)

    def get_search_results(self, request, queryset, search_term):
        if search_term:
            queryset = queryset.filter(
                Q(name__icontains=search_term) |
                Q(uid=search_term)
            )
        may_have_duplicates = False

        return queryset, may_have_duplicates


@dj_admin.register(Component)
class ComponentAdmin(NodeModelAdmin):
    # ComponentAdmin form is necessary for the dropdown menu to choose the Component type
    # form = ComponentAdminForm
    # list_display determines which properties are displayed
    list_display = ["uid"]

    # save function, necessary to save instances
    def save(self, commit=True):
        instance = super().save(commit)
        instance.user_skill = True
        instance.save()

        return instance


@dj_admin.register(Device)
class DeviceAdmin(NodeModelAdmin):
    form = DeviceAdminForm
    list_display = ("uid",
                    "name")
