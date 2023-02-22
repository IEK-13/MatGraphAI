from Mat2DevAPI.models.metadata import Researcher
from Mat2DevAPI.admins.adminBase import (NodeModelAdmin)
from django.contrib import admin as dj_admin


@dj_admin.register(Researcher)
class ResearcherAdmin(NodeModelAdmin):
    class Meta:
        pass
    # displays the "name" and "abbreviation" on the admin site
    list_display = ("name", "ORCID", "email")