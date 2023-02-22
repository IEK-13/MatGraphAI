"""All admin classes that are required for "matter" models. Contains Typefilters, to allow filtering of "matter"
classes by certain properties and the model admins. AdminClasses register the models on the admin site and allow
reading writing and deleting of their instances via the admin interface """

from django.contrib import admin as dj_admin
from django.contrib.admin import SimpleListFilter

from Mat2DevAPI.admins.adminBase import (NodeModelAdmin)
from Mat2DevAPI.choices.ChoiceFields import COMPONENT_TYPE_CHOICES
from Mat2DevAPI.forms.adminForms import ComponentAdminForm, MoleculeAdminForm, MaterialAdminForm
from Mat2DevAPI.models.processes import Measurement

@dj_admin.register(Measurement)
class MeasurementAdmin(NodeModelAdmin):
    list_display = ("uid",)

    def save(self, commit=True):
        instance = super().save(commit)
        instance.user_skill = True
        instance.save()

        return instance

    actions = ['delete_model']
