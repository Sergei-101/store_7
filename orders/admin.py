from django.contrib import admin
from orders.models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']



class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_customer_name', 'status', 'total_cost', 'created']
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
