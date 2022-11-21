from django.contrib import admin as dj_admin

from Mat2DevAPI.admins.adminBase import NodeModelAdmin
from Mat2DevAPI.forms.adminForms import ComponentAdminForm
from Mat2DevAPI.models.properties import Quantity


@dj_admin.register(Quantity)
class PropertyAdmin(NodeModelAdmin):
    list_display = ("uid",)

    def save(self, commit=True):
        instance = super().save(commit)
        instance.user_skill = True
        instance.save()

        return instance

    actions = ['delete_model']

