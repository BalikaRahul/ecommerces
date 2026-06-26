from django.contrib import admin
from .models import Product,Variation


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('product_name',)}# that comma is very important because this is a tuple ds
    list_display = ('product_name','price','stock','category','modified_date','is_avaliable')
    

# Register your models here.
admin.site.register(Product,ProductAdmin) #to automate the slug need the call the object
class VariationAdmin(admin.ModelAdmin):
    list_display=('Product','variation_category','variation_value','is_active')
    list_editable=('is_active',)
    list_filter=('Product','variation_category','variation_value',)
admin.site.register(Variation,VariationAdmin)