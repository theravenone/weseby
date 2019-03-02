from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import *

# Register your models here.


class LakiAdmin(ImportExportModelAdmin):
    list_display = ('vorname', 'nachname', 'zelt')
    list_filter = ['zelt']
    search_fields = ['vorname', 'nachname']


@admin.register(Zelt)
class ZeltAdmin(ImportExportModelAdmin):
    pass

# admin.site.register(Zelt)
admin.site.register(Laki, LakiAdmin)
admin.site.register(Konto)
admin.site.register(Zeltlager)
