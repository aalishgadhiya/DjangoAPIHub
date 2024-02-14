from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserRegistrationSerializer,UserLoginSerializer
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from account.models import Users




# Creating tokens manually 
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request):
        serializer  = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token},status=status.HTTP_201_CREATED,headers={'message':'Registration success'})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST,headers={'message':'Registration Failed'})
    
    
class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email_or_username = serializer.data.get('email_or_username')
            password = serializer.data.get('password')

            user = Users.objects.filter(email = email_or_username).first()
            if not user:
                user = Users.objects.filter(username = email_or_username).first()

            if user is not None:
                user = authenticate(request,username=user,password=password)
                if user is not None:
                    token = get_tokens_for_user(user)
                    message = 'Login Success'
                    return Response({'token':token},status=status.HTTP_201_CREATED,headers={'message':message})
                
            return Response({'non_fields_errors':['Email/Username or password is not valid']},status=status.HTTP_400_BAD_REQUEST,headers={'message':'Login Failed'})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST,headers={'message':'Login Failed'})    
            
            
            
                
                        
        
    