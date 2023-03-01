from neomodel import RelationshipTo, StringProperty, ArrayProperty

from Mat2DevAPI.forms.formsMetadata import ResearcherAdminForm, InstitutionAdminForm
from Mat2DevAPI.models.metadata import Researcher, Institution, Instrument
from Mat2DevAPI.admins.adminBase import (NodeModelAdmin)
from django.contrib import admin as dj_admin


@dj_admin.register(Instrument)
class ResearcherAdmin(NodeModelAdmin):
    class Meta:
        pass
    # displays the "name" and "abbreviation" on the admin site
    list_display = ("name", "uid")

@dj_admin.register(Researcher)
class ResearcherAdmin(NodeModelAdmin):
    class Meta:
        pass
    # displays the "name" and "abbreviation" on the admin site
    list_display = ("name", "ORCID", "email", "uid")
    form = ResearcherAdminForm

@dj_admin.register(Institution)
class InstitutionAdmin(NodeModelAdmin):
    class Meta:
        pass
    # displays the "name" and "abbreviation" on the admin site
    list_display = ("name", "ROI", "link", "uid")
    form  = InstitutionAdminForm
    search_fields = ('name',)
