from rest_framework import serializers
from account.models import Users,Companies,Employees


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
        fields = ['id','username','first_name','last_name','email','gender','password']     
        
        
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id','username','first_name','last_name','email','gender','password','is_admin']     
    
    
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users     
        fields = ['id','username','first_name','last_name','email','gender','password','is_admin']     



class CompanySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = Companies
        fields = '__all__'
               
        
class EmployeeSerializer(serializers.ModelSerializer):     
    id = serializers.ReadOnlyField()
    company_id = serializers.PrimaryKeyRelatedField(queryset=Companies.objects.all(), source='company', write_only=True)
    company = CompanySerializer(read_only=True)
    class Meta:
        model = Employees
        fields = '__all__'


class CompanyEmployeeSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()
    class Meta:
      model = Employees
      fields = '__all__'