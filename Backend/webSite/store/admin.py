from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('product_name',)}# that comma is very important because this is a tuple ds
    list_display = ('product_name','price','stock','category','modified_date','is_avaliable')
    

# Register your models here.
admin.site.register(Product,ProductAdmin) #to automate the slug need the call the object