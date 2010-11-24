from django.contrib import admin

from clientinfo.models import Url

class UrlAdmin(admin.ModelAdmin):
    fields = ['id', 'uri', 'created_on']
    readonly_fields = ['id', 'created_on']

admin.site.register(Url, UrlAdmin)
