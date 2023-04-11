import csv

def import_csv(modeladmin, request, queryset):
    for obj in queryset:
        csv_data = csv.reader(obj.file.read().decode('utf-8').splitlines())
        json_data = []
        header = None
        for row in csv_data:
            if not header:
                header = row
            else:
                data = {}
                for i in range(len(header)):
                    data[header[i]] = row[i]
                json_data.append(data)
        # Do something with the JSON data
import_csv.short_description = "Import selected CSV files"

from django.contrib import admin
from .models import CsvFile

class CsvFileAdmin(admin.ModelAdmin):
    list_display = ('file',)
    actions = [import_csv]

admin.site.register(CsvFile, CsvFileAdmin)
