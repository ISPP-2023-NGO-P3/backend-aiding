from django.contrib import admin
from rest_framework.response import Response

from .models import Item, Type


class TypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)


class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "quantity","type")
    list_filter = ("name",)
    search_fields = ("name",)


admin.site.register(Type, TypeAdmin)
admin.site.register(Item, ItemAdmin)
