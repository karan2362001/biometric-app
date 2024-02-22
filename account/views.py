from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login
from django.contrib import messages 
from django.http import HttpResponse
from account.models import User
from account.serializers import UserSerializer
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
import requests


class UserRegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self,request,*args,**kwargs):
        data=User.objects.all()
        get_data=UserSerializer(data,many=True)
        return Response(get_data.data) 



class UserLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            if created:
                token.delete()  # Delete the token if it was already created
                token = Token.objects.create(user=user)
            return Response({'token': token.key, 'username': user.username, 'role': user.role})
        else:
            return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)



class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        print(request.headers) 
        token_key = Token.objects.get(user__id=request.user.id).key
        token = Token.objects.get(key=token_key)
        token.delete()

        return Response({'detail': 'Successfully logged out.'})



# Create your views here.
def homepage(request):
    return render(request,"homepage.html")

def logout(request):
    auth.logout(request)
    return render(request,"homepage.html")

def signin(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
       # data={"username":username,"password":password}
        #api_url="http://127.0.0.1:8000/api/auth/login/"
        #response = requests.post(api_url, data=data)
       # print(response.text)
 
        user=auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('homepage')
        else:
            messages.info(request,"invalid credentials...")
            return redirect('signin')
    else:
        return render(request,"signin.html")
  

def signup(request):
    if request.method == "POST":
        
        username=request.POST['username']
        password=request.POST['password']
        password2=request.POST['password2']
        email=request.POST['email']
        data={"username":username,"email":email,"password":password,"role":"admin"}

        #Checking if the user is already registered or not
        if password==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email Already Registered')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username Already Taken')
                return redirect('signup')
            else:
                api_url="http://127.0.0.1:8000/api/auth/register/"
                response = requests.post(api_url, data=data)
                #user=User.objects.create_user(username=username,password=password,email=email)
                #user.save()
                return redirect('signin')
        else:
            messages.info(request,"password is not same")
            return redirect('signup')
    else:
        return render(request,'signup.html')