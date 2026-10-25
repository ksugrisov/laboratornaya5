from django.contrib import admin
from .models import Advert


class AdvertAdmin(admin.ModelAdmin):
    list_display = ('title', 'customer', 'program', 'air_date', 'get_cost', 'get_excerpt', 'created_date')


admin.site.register(Advert, AdvertAdmin)
