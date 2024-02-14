from django.contrib import admin
from account.models import Users
from django.contrib.auth.admin import UserAdmin



# Register your models here.

class UserModelAdmin(UserAdmin):


    list_display = ['id','username','first_name','last_name','email','gender','is_admin']
    list_filter = ["is_admin"]
    fieldsets = [
        ('user Credentials', {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["username",'first_name','last_name','gender']}),
        ("Permissions", {"fields": ["is_admin"]}),

    ]

    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "username",'first_name','last_name','gender', 'password1', 'password2']
            },
        ),
    ]
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ["email"]
    filter_horizontal = []


admin.site.register(Users, UserModelAdmin)

