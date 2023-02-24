"""All admin classes that are required for "matter" models. Contains Typefilters, to allow filtering of "matter"
classes by certain properties and the model admins. AdminClasses register the models on the admin site and allow
reading writing and deleting of their instances via the admin interface """

from django.contrib import admin as dj_admin

from Mat2DevAPI.admins.adminBase import (NodeModelAdmin)
from Mat2DevAPI.forms.adminForms import ManufacturingAdminForm
from Mat2DevAPI.models.processes import Measurement, Manufacturing


@dj_admin.register(Measurement)
class MeasurementAdmin(NodeModelAdmin):
    list_display = ("uid",)

    def save(self, commit=True):
        instance = super().save(commit)
        instance.user_skill = True
        instance.save()

        return instance

    actions = ['delete_model']


@dj_admin.register(Manufacturing)
class ManufacturingAdmin(NodeModelAdmin):
    list_display = ("uid",)

    def save(self, commit=True):
        instance = super().save(commit)
        instance.user_skill = True
        instance.save()

        return instance
    form = ManufacturingAdminForm
    actions = ['delete_model']
