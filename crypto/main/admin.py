from django.contrib import admin

from main.models import Detail, Crypto


class YourModelAdmin(admin.ModelAdmin):
    list_filter = [
        'currency',
    ]
    search_fields = (
        'currency_name',
    )


admin.site.register(Detail, YourModelAdmin)
admin.site.register(Crypto)
