from django.contrib import admin
from account.models import Users,Companies,Employees,Departments
from django.contrib.auth.admin import UserAdmin



# Register your models here.

class UserModelAdmin(UserAdmin):


    list_display = ['id','username','first_name','last_name','email','gender','is_admin','created','updated']
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
    list_display=('id','name','location','about','type','active','created','updated')
    
class EmployeeAdmin(admin.ModelAdmin):
    list_display=('id','name','email','address','phone','about','position','company','department','created','updated')
    

class DepartmentAdmin(admin.ModelAdmin):
    list_display=('id','name','description','company','created','updated')
            
            
admin.site.register(Companies,CompanyAdmin)    
admin.site.register(Employees,EmployeeAdmin)
admin.site.register(Departments,DepartmentAdmin)