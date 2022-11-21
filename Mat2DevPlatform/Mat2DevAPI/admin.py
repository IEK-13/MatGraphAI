from Mat2DevAPI.admins.adminMatter import *
from Mat2DevAPI.admins.adminProperties import *
from Mat2DevAPI.models.metadata import (Researcher)
from Mat2DevAPI.models.processes import (Manufacturing,
                                         Measurement)






@dj_admin.register(Researcher)
class ResearcherAdmin(dj_admin.ModelAdmin):
    list_display = ("name",)


@dj_admin.register(Measurement)
class MeasurementAdmin(dj_admin.ModelAdmin):
    list_display = ("uid",)


@dj_admin.register(Manufacturing)
class ManufacturingAdmin(dj_admin.ModelAdmin):
    list_display = ("uid",)
