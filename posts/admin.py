from django.contrib import admin
from posts.models import Post, Category
admin.site.register(Post)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',) # отоброжать поля
    prepopulated_fields = {'slug': ('name',)}
    

