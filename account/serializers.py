from rest_framework import serializers
from account.models import Users,Companies,Employees,Departments


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
         model = Users
         fields = ['id','username','first_name','last_name','email','gender','password','password2']
         extra_kwargs={
             'password':{'write_only':True}
         }
         
         
    def validate(self,data):
        password = data.get('password')
        password2 = data.get('password2')
        
        if password != password2:
            raise serializers.ValidationError("password and confrim password doesn't match")
        
        return data
         
         
    def create(self, validated_data):
          return Users.objects.create_user(**validated_data)
      
      
      
      
class UserLoginSerializer(serializers.ModelSerializer):
    email_or_username = serializers.CharField(max_length=255,required=True)
    class Meta:
        model = Users
        fields = ['email_or_username','password']
        
        

        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id','username','first_name','last_name','email','gender','password','created','updated']     
        
        
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id','username','first_name','last_name','email','gender','password','is_admin','created','updated']     
    
    
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users     
        fields = ['id','username','first_name','last_name','email','gender','password','is_admin','created','updated']     



class CompanySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = Companies
        fields = '__all__'
               


class DepartmentSerializer(serializers.ModelSerializer):
    company_id = serializers.PrimaryKeyRelatedField(queryset=Companies.objects.all(), source='company', write_only=True)
    company = CompanySerializer(read_only=True)
    class Meta:
        model = Departments
        fields = '__all__' 
        
        
    def validate(self, data):
        company = data.get('company')
        name = data.get('name')
        
        # Check if company is provided
        if company is None:
            raise serializers.ValidationError('company_id Field Is Required')
        
        # Check if department name is provided
        if name is None:
            raise serializers.ValidationError('name Field Is Required')
        
        # Get department instance if available (for update)
        instance = self.instance
        if instance:
            # If the department name is being updated, check for uniqueness within the company
            if name != instance.name:
                existing_department = Departments.objects.exclude(id=instance.id).filter(company=company, name=name)
                if existing_department.exists():
                    raise serializers.ValidationError('A department with this name already exists in the company.')
        
        # If creating a new department, check if a department with the same name exists in the company
        else:
            existing_department = Departments.objects.filter(company=company, name=name)
            if existing_department.exists():
                raise serializers.ValidationError('A department with this name already exists in the company.')

        return data


        
class EmployeeSerializer(serializers.ModelSerializer):     
    id = serializers.ReadOnlyField()
    company_id = serializers.PrimaryKeyRelatedField(queryset=Companies.objects.all(), source='company', write_only=True)
    # company = CompanySerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(queryset=Departments.objects.all(),source='department', write_only=True)
    
    class Meta:
        model = Employees
        exclude = ['company']
        
    def validate(self, data):
        company = data.get('company')
        department = data.get('department_id')
        
        if company and department:
            if department.company != company:
                raise serializers.ValidationError('Department does not belong to the provided company')
            
        return data


class CompanyEmployeeSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()
    department = serializers.StringRelatedField()
    class Meta:
      model = Employees
      fields = '__all__'
      


class CompanyDepartmentSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()
    class Meta:
        model = Departments
        fields = '__all__'
        

class DepartmentEmployeeSerializer(serializers.ModelSerializer):
    # company = CompanySerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    class Meta:
        model = Employees
        exclude = ['company']       