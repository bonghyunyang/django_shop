from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_user', 'product')


admin.site.register(Order, OrderAdmin)
