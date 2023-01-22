from django.contrib import admin
from .models import NippoModel

class NippoModelAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "public",
        "date",
        "slug",
        "timestamp"
    )
    list_filter = (
        "date",
        "user",
        "public"
    )
    ordering = ("date","timestamp","user")
    filter_horizontal = ()
    
    search_fields = ('title',"content","user")

admin.site.register(NippoModel, NippoModelAdmin)
