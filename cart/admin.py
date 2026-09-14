from django.contrib import admin
from .models import Order, Item


class ItemInline(admin.TabularInline):
    model = Item
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total', 'date']
    search_fields = ['user__username']
    inlines = [ItemInline]


admin.site.register(Order, OrderAdmin)
admin.site.register(Item)
