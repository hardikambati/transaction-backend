from django.contrib import admin

# custom
from . import models


class CustomATransactionAdmin(admin.ModelAdmin):
    readonly_fields = ("txn_id",)

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields
    

admin.site.register(models.Transaction, CustomATransactionAdmin)