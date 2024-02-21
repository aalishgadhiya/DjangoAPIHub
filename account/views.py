from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserRegistrationSerializer,UserLoginSerializer,UserProfileSerializer,UserListSerializer,UserDetailSerializer,CompanySerializer,EmployeeSerializer,CompanyEmployeeSerializer,DepartmentSerializer,CompanyDepartmentSerializer,DepartmentEmployeeSerializer
from account.renderers import UserRenderer,CustomJSONRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from account.models import Users,Companies,Employees,Departments
from rest_framework.permissions import IsAuthenticated



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
    
        errors = serializer.errors
        if 'username' in errors and 'users with this username already exists.' in errors['username']:
            status_code = status.HTTP_409_CONFLICT
        elif 'email' in errors and 'users with this Email already exists.' in errors['email']:
            status_code = status.HTTP_409_CONFLICT
        else:
            status_code = status.HTTP_400_BAD_REQUEST

        return Response(errors, status=status_code, headers={'message': 'Registration Failed'})
    
    
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
                
            return Response({'non_fields_errors':['Email/Username or password is not valid']},status=status.HTTP_401_UNAUTHORIZED,headers={'message':'Login Failed'})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST,headers={'message':'Login Failed'})    
            
  

            
       
class UserProfileView(APIView):
    renderer_classes = [CustomJSONRenderer]     
    permission_classes = [IsAuthenticated]   
    def get(self,request):
        serializer = UserProfileSerializer(request.user)
        
        return Response({'user':serializer.data},status=status.HTTP_200_OK)     
                        
        

# user list-view ---------
class UserListView(APIView):
    renderer_classes = [CustomJSONRenderer] 
    permission_classes = [IsAuthenticated]       
    def get(self,request):
        User_data = Users.objects.all()
        serializer = UserListSerializer(User_data,many=True)
        return Response({'users':serializer.data},status=status.HTTP_200_OK)  
    
    
    
class UserDetailView(APIView):
    renderer_classes = [CustomJSONRenderer] 
    permission_classes = [IsAuthenticated]   
    def get(self,request,user_id):
        try:
            user = Users.objects.get(id=user_id)
            serializer = UserDetailSerializer(user)
            return Response({'user':serializer.data},status=status.HTTP_200_OK)
        except Users.DoesNotExist:
            return Response({'message':'User Not Found'},status=status.HTTP_404_NOT_FOUND)
        
    def patch(self,request,user_id):
        try:
            user = Users.objects.get(id=user_id)
            data = request.data
            data.pop('id', None)
            data.pop('username', None)
            data.pop('email', None)
            data.pop('password', None)
            data.pop('is_admin', None)
            serializer = UserDetailSerializer(user,data=data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'user':serializer.data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Users.DoesNotExist:
            return Response({'message':'User Not Found'},status=status.HTTP_404_NOT_FOUND)
        
    def delete(self,request,user_id):
        try: 
            user = Users.objects.get(id=user_id)
            user.delete()
            return Response({'message':'user deleted successfully'},status=status.HTTP_204_NO_CONTENT)
        
        except Users.DoesNotExist:
            return Response({'message':'User Not Found'},status=status.HTTP_404_NOT_FOUND) 
        
    
       
# Company List View ----------
class CompanyListView(APIView):
    renderer_classes = [CustomJSONRenderer]
    permission_classes = [IsAuthenticated]   

    def get(self,request):
        type_filter = request.query_params.get('type')
        if type_filter:
            companies = Companies.objects.filter(type=type_filter)
        else:    
            companies = Companies.objects.all()
            
        serializer = CompanySerializer(companies,many=True)
        return Response({'Companies':serializer.data},status=status.HTTP_200_OK)
    def post(self,request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response({'Company':serializer.data},status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
                        
class CompanyDetailView(APIView):
    renderer_classes = [CustomJSONRenderer]

    def get(self,request,company_id):
        try:
            company = Companies.objects.get(id=company_id)
            serializer = CompanySerializer(company)
            return Response({'Company':serializer.data},status=status.HTTP_200_OK)
        
        except Companies.DoesNotExist:
            return Response({'message':'Company Not Found'},status=status.HTTP_404_NOT_FOUND)
        
    
    def patch(self,request,company_id):
        try:
            company = Companies.objects.get(id=company_id)
            data = request.data
            serializer = CompanySerializer(company,data=data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'Company':serializer.data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Companies.DoesNotExist:
            return Response({'message':'Company Not Found'},status=status.HTTP_404_NOT_FOUND)   
        
        
    def delete(self,request,company_id):
        try:
            company = Companies.objects.get(id=company_id)
            company.delete()     
            return Response({'message':'Company deleted successfully'},status=status.HTTP_204_NO_CONTENT)
        
        except Companies.DoesNotExist:
            return Response({'message':'Company Not Found'},status=status.HTTP_404_NOT_FOUND)   
        
                



class CompanyEmployeeListView(APIView):
    renderer_classes = [CustomJSONRenderer]
    permission_classes = [IsAuthenticated]   
    def get(self,request,company_id):
        try:
            company = Companies.objects.get(id=company_id)
            employees = Employees.objects.filter(company=company_id)
            serializer = CompanyEmployeeSerializer(employees, many=True)
            return Response({'employees':serializer.data},status=status.HTTP_200_OK)
        except Companies.DoesNotExist:
            return Response({'message':'Company Not Found'},status=status.HTTP_404_NOT_FOUND)
        
        
        

class CompanyDepartmentListView(APIView):
    renderer_classes = [CustomJSONRenderer]
    
    def get(self,request,company_id):
        try:
            department = Departments.objects.filter(company=company_id)
            serializer = CompanyDepartmentSerializer(department,many=True)
            return Response({'Departments':serializer.data},status=status.HTTP_200_OK)
        except Companies.DoesNotExist:
              return Response({'message':'Company Not Found'},status=status.HTTP_404_NOT_FOUND)  
          
          
          
class DepartmentEmployeeList(APIView):
     renderer_classes = [CustomJSONRenderer]      
     
     def get(self,request,department_id):
         try:
            employee = Employees.objects.filter(department=department_id)
            serializer = DepartmentEmployeeSerializer(employee,many=True)
            return Response({'Employees':serializer.data},status=status.HTTP_200_OK)
         
         except Departments.DoesNotExist:
              return Response({'message':'Department Not Found'},status=status.HTTP_404_NOT_FOUND) 
                

 # Employee List View ---------
 
class EmployeeListView(APIView):
    renderer_classes = [CustomJSONRenderer]
    permission_classes = [IsAuthenticated]   

    def get(self,request):
        employee = Employees.objects.all()
        serializer = EmployeeSerializer(employee,many=True)
        return Response({'Employees':serializer.data},status=status.HTTP_200_OK)
    def post(self,request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Employee':serializer.data},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

      
        
class EmployeeDetailView(APIView):
    renderer_classes = [CustomJSONRenderer]
    def get(self,request,employee_id):
        try:
            employee = Employees.objects.get(id=employee_id)
            serializer = EmployeeSerializer(employee)
            return Response({'Employee':serializer.data},status=status.HTTP_200_OK)      
        
        except Employees.DoesNotExist:
            return Response({'message':'Employee Not Found'},status=status.HTTP_404_NOT_FOUND)    
        
        
    def patch(self,request,employee_id):
        try:
            employee = Employees.objects.get(id=employee_id)
            data = request.data        
            serializer = EmployeeSerializer(employee,data=data,partial=True)   

            if serializer.is_valid():
                serializer.save()
                return Response({'Employee':serializer.data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Employees.DoesNotExist:
            return Response({'message':'Employee Not Found'},status=status.HTTP_404_NOT_FOUND)    
        
    def delete(self,request,employee_id):
        try:
            employee = Employees.objects.get(id=employee_id)
            employee.delete()
            return Response({'message':'Employee deleted successfully'},status=status.HTTP_204_NO_CONTENT)        
         
        except Employees.DoesNotExist:
            return Response({'message':'Employee Not Found'},status=status.HTTP_404_NOT_FOUND)   




# departments API 



class DepartmentListView(APIView):
    renderer_classes = [CustomJSONRenderer]
    
    def get(self,request):
        departments = Departments.objects.all()
        serializer = DepartmentSerializer(departments,many=True)
        return Response({'Departments':serializer.data},status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Department':serializer.data},status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class DepartmentDetailView(APIView):
    renderer_classes = [CustomJSONRenderer]
    
    def get(self,request,department_id):
        try:
            department = Departments.objects.get(id=department_id)
            serializer = DepartmentSerializer(department)
            return Response({'Department':serializer.data},status=status.HTTP_200_OK)
        
        except Departments.DoesNotExist:
            return Response({'message':'Department Not Found'},status=status.HTTP_404_NOT_FOUND)  
    
    
    def patch(self,request,department_id):
        try:
            department = Departments.objects.get(id=department_id)
            data= request.data 
            serializer = DepartmentSerializer(department,data=data,partial=True)   
            
            if serializer.is_valid():
                serializer.save()
                return Response({'Department':serializer.data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)       
        
        except Departments.DoesNotExist:
            return Response({'message':'Department Not Found'},status=status.HTTP_404_NOT_FOUND)
        
    
    
    def delete(self,request,department_id):
        try:
            department = Departments.objects.get(id=department_id)
            department.delete()
            return Response({'message':'Department deleted successfully'},status=status.HTTP_204_NO_CONTENT)
        
        except Departments.DoesNotExist:
            return Response({'message':'Department Not Found'},status=status.HTTP_404_NOT_FOUND) 
                    
             
    