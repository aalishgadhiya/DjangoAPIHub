from rest_framework import serializers
from account.models import Users


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
        