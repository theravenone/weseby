from django.contrib import admin

from .models import *

# Register your models here.


class LakiAdmin(admin.ModelAdmin):
    list_display = ('vorname', 'nachname', 'zelt')
    list_filter = ['zelt']
    search_fields = ['vorname', 'nachname']

admin.site.register(Zelt)
admin.site.register(Laki, LakiAdmin)
admin.site.register(Konto)
admin.site.register(Zeltlager)
