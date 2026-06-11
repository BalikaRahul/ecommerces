from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account
# This class helps to stop edit the password in the admin
class AccountAdmin(UserAdmin):
    list_display=('email','first_name','last_name','username','last_login','date_joined','is_active')
    list_display_links =('email','first_name','last_name')# it help to click the attribute to go further
    readonly_fields =('last_login','date_joined') # to stop edit 
    ordering=('-date_joined',)# comma is impotant if comma is removed error will come
    # there the rules while using custom auth model
    filter_horizontal =()
    list_filter = ()
    fieldsets = ()

# Register your models here.
admin.site.register(Account,AccountAdmin)
