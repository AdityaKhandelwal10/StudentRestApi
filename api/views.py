from django.shortcuts import render
from . models import Student, StudentVerification
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import(
    
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response    
from .serializers import RegisterSerializer
from rest_framework import generics
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views import View
import random, json
from django.conf import settings
from django.core.mail import send_mail

#9d26a52cf7fe021360005617525a5891b2fc939143e60beb67f4faf7ed1a6736

@csrf_exempt
@api_view(["POST"])
#@permission_classes((permissions.AllowAny,))
def login(request):

    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)

class RegisterView(generics.CreateAPIView):
    queryset = Student.objects.all()
    permission_classes =(AllowAny,)
    serializer_class = RegisterSerializer

class Register(View):
    def get(self, request):
        student_list = list(Student.objects.values())
        return JsonResponse(student_list, safe=False)


    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(Register, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        student_data1 = request.body.decode('utf-8')
        student_data = json.loads(student_data1)


        try:
            password = student_data.get('password')
            new_student  = Student(username = student_data["username"], email = student_data["email"])
            new_student.set_password(password)
            new_student.is_active = 0 
            new_student.save()
            otp = random.randint(1111,9999)
           
            #email starts here
            subject = "Please verify your account through this otp"
            message =f"Hi {new_student.username}, here is your otp - " + str(otp)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [new_student.email,]

            send_mail(subject, message , email_from , recipient_list)

            #registering user to the student verification table
            # student_object = Student.objects.get(username = new_student.username)
            StudentVerification.objects.create(student_id = new_student, otp = otp)

            return JsonResponse({"Mail Sent to": student_data}, safe = False)
        
        except Exception as e:
            return JsonResponse({"Error": str(e)}, safe = False)

    
            
    # def VerifyOTP(self, a, b):
    #     if (a == b):
    #         return True
        
    #     else : False

class Verify(View):

   
    #requires username, otp
    def post(self, request):
        data1 = request.body.decode('utf-8')
        data = json.loads(data1)

        try:
            student = Student.objects.get(username = data["username"])
            sv_object = StudentVerification.objects.get(student_id = student.pk)
            given_otp = data["otp"]
            ass_otp = sv_object.otp

            if(ass_otp == given_otp):
                sv_object.is_active = 1
                sv_object.save()
                student.is_active = 1 
                student.save()

                return JsonResponse({"Success" : "User and mail authenticated"})


            else:

                return JsonResponse({"Error" : "The otp does not match pls try again"})
        
        except Exception as e :
            return JsonResponse({"Error": str(e)}, safe = False)

            

class loginview(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(loginview,self).dispatch(request, *args , **kwargs)

    # takes in the username and password, first checks if the user is active or not
    def post(self, request):
        login_data1 = request.body.decode('utf-8')
        login_data = json.loads(login_data1)
        
        try:
            username = login_data.get('username')
            password = login_data.get('password')
            
            student = authenticate(username = username, password = password)

            if student is not None:
                if (student.is_active ):
                    login(request,student)
                    return JsonResponse({"Successful login" : student.username, "Mail" : student.email})

                else :
                    return JsonResponse({"Error" : "Please verify your email first"})

            else :
                JsonResponse({"Unsuccessful login" : "Please check again"}) 

        except Exception as e:
             return JsonResponse({"Error": str(e)}, safe = False)



class logoutview(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(logoutview,self).dispatch(request, *args , **kwargs)

    @method_decorator(login_required)
    def post(self,request):
        logout(request)

            
