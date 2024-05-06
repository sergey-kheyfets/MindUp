from django.contrib import admin

from .models import Guest, Organization, Meeting

admin.site.register(Guest)
admin.site.register(Organization)
admin.site.register(Meeting)
