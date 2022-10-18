from django.contrib import admin as dj_admin
from django_neomodel import admin as neo_admin

from Mat2DevAPI.models.matter import MEA

class MEAAdmin(dj_admin.ModelAdmin):
    list_display = ("name",)

neo_admin.register(MEA, MEAAdmin)