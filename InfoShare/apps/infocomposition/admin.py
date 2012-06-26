from django.contrib import admin 
from apps.infocomposition.models import *

class InfoCompositionAdmin(admin.ModelAdmin):
    search_fields = ["name","tags"]

    def save_model(self, request, obj, form, change): 
        obj.user = request.user
        obj.save()

class TagAdmin(admin.ModelAdmin):
    search_fields = ["tag"]

admin.site.register(InfoComposition,InfoCompositionAdmin)
admin.site.register(Tag,TagAdmin)
