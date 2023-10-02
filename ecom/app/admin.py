from django.contrib import admin
from .models import *

# Register your models here.

# class AdminCategory(admin.ModelAdmin):
#     list_display = ('Name',)
    
# class AdminSubCategory(admin.ModelAdmin):
#     list_display = ('Name', 'Category')


admin.site.register(Categories)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(contactus)
admin.site.register(order)
admin.site.register(Brand)

