from django.contrib import admin
from django.utils.safestring import mark_safe
from orders.models import Order, OrderItem
from django.urls import reverse

def order_detail(obj):
    url = reverse('orders:admin_order_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">Детали</a>')
    

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    autocomplete_fields = ['product']


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity']
    search_fields = ['id', 'order']

admin.site.register(OrderItem, OrderItemAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_customer_name', 'status', 'total_cost', 'created', order_detail]
    list_filter = ['status', 'customer_type']
    search_fields = ['id', 'company_name', 'contact_person', 'email', 'phone_number']
    inlines = [OrderItemInline]


    def get_customer_name(self, obj):
        if obj.customer_type == 'personal':
            return f'{obj.contact_person} '
        elif obj.customer_type == 'business':
            return obj.company_name
        return '-'
    get_customer_name.short_description = 'Customer Name'

admin.site.register(Order, OrderAdmin)

