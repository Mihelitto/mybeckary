from django.contrib import admin
from .models import Product, Section, Category

#admin.site.register(Product)
#admin.site.register(Section)
#admin.site.register(Category)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    #prepopulated_fields = {'slug':('name',)}

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    #prepopulated_fields = {'slug':('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price']
    #prepopulated_fields = {'slug':('name',)}


# Register your models here.
