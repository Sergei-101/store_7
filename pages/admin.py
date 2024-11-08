# admin.py
from django.contrib import admin
from pages.models import Guarantee, SliderItem, StaticPage, Tab
from pages.forms import StaticPageForm

class StaticPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    form = StaticPageForm  # Указываем кастомную форму с CKEditor

admin.site.register(StaticPage, StaticPageAdmin)

admin.site.register(Guarantee)
admin.site.register(SliderItem)
admin.site.register(Tab)
