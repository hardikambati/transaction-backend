from django.contrib import admin

# custom
from . import models


class CustomAccountsAdmin(admin.ModelAdmin):
    readonly_fields = ("value",)

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields
    

admin.site.register(models.AccessToken, CustomAccountsAdmin)
admin.site.register(models.Connections)
