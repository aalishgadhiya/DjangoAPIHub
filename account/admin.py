from django.contrib import admin
from account.models import Users,Companies,Employees
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



class CompanyAdmin(admin.ModelAdmin):
    list_display=('id','name','location','about','type','added_date','active')
    
class EmployeeAdmin(admin.ModelAdmin):
    list_display=('id','name','email','address','phone','about','position','company')
    
        
admin.site.register(Companies,CompanyAdmin)    
admin.site.register(Employees,EmployeeAdmin)
