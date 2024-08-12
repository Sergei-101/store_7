from django.contrib import admin

from pages.models import Content, Section

admin.site.register(Content)


@admin.register(Section)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',) # отоброжать поля
    prepopulated_fields = {'slug': ('name',)}