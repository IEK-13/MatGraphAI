from Mat2DevAPI.forms.adminForms import ManufacturingAdminForm
from Mat2DevAPI.models.ontology import EMMO_Process
from django.contrib import admin as dj_admin
from Mat2DevAPI.admins.adminBase import (NodeModelAdmin)

@dj_admin.register(EMMO_Process)
class EMMO_ProcessAdmin(NodeModelAdmin):
    list_display = ("EMMO__name", "uid")

    def save(self, commit=True):
        instance = super().save(commit)
        instance.save()

        return instance
    actions = ['delete_model']