from django.contrib import admin as dj_admin
from django.contrib.admin import SimpleListFilter

from Mat2DevAPI.admins.base import (NodeModelAdmin)
from Mat2DevAPI.choices.ChoiceFields import COMPONENT_TYPE_CHOICES
from Mat2DevAPI.forms.adminForms import ComponentAdminForm
from Mat2DevAPI.models.matter import (Element,
                                      Molecule,
                                      Component,
                                      Device)


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


@dj_admin.register(Element)
class ElementAdmin(dj_admin.ModelAdmin):
    class Meta:
        pass

    list_display = ("uid",)


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
                    "charge"
                    )


@dj_admin.register(Device)
class DeviceAdmin(dj_admin.ModelAdmin):
    list_display = ("uid",)
