from django.contrib import admin as dj_admin

from Mat2DevAPI.admins.adminBase import (NodeModelAdmin)
from Mat2DevAPI.models.ontology import EMMOProcess, EMMOMatter


@dj_admin.register(EMMOProcess)
class EMMOProcessAdmin(NodeModelAdmin):
    list_display = ("EMMO__name", "uid")

    def save(self, commit=True):
        instance = super().save(commit)
        instance.save()

        return instance
    actions = ['delete_model']

@dj_admin.register(EMMOMatter)
class EMMOMatterAdmin(NodeModelAdmin):
    list_display = ("EMMO__name", "uid")

    def save(self, commit=True):
        instance = super().save(commit)
        instance.save()

        return instance
    actions = ['delete_model']