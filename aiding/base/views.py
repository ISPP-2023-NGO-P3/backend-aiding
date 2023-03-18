import json
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt

from rest_framework import views
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK as ST_200,
    HTTP_201_CREATED as ST_201,
    HTTP_401_UNAUTHORIZED as ST_401,
    HTTP_403_FORBIDDEN as ST_403,
    HTTP_404_NOT_FOUND as ST_404
)

from .models import User

class LoginView(views.APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @method_decorator(csrf_exempt)
    def post(self, request):
        if request.user.is_authenticated:
            data = {'message' : 'You are already logged in!'}
            return Response(data, status=ST_401)
        jd = json.loads(request.body)
        user = authenticate(username = jd['username'], password = jd['password'])
        if user is not None:
            login(request, user)
            data = {'message' : 'Login successful!'}
            return Response(data, status=ST_200)
        else:
            data = {'message' : 'Login unsuccessful'}
            return Response(data, status=ST_401)

class LogoutView(views.APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
            data = {'message' : 'Logout successful!'}
        else:
            data = {'message' : 'You are not logged in!'}
        return Response(data, status=ST_200)

class UserView(views.APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, user_id = 0):
        if (user_id > 0):
            users = list(User.objects.filter(id=user_id).values())
            if len(users) > 0:
                user = users[0]
                return Response(data=user, status=ST_200)
            else:
                data = {'message': "user not found..."}
                return Response(data=data, status=ST_404)
        else:
            users = list(User.objects.values())
            if len(users) > 0:
                return Response(data=users, status=ST_200)
            else:
                data = {'message': "users not found..."}
                return Response(data=data, status=ST_404)

    def post(self, request):
        jd = json.dumps(request.data)
        jd = json.loads(jd)
        auth_user = request.user
        if auth_user.is_authenticated and auth_user.is_admin:            
            User.objects.create(username=jd['username'],password=make_password(jd['password']))
            data = {'message': "Success"}
            return Response(data=data, status=ST_201)
        else:
            data = {'message': "You do not have permissions."}
            return Response(data=data, status=ST_403)

    def put(self, request, user_id):
        jd = json.dumps(request.data)
        jd = json.loads(jd)
        users = list(User.objects.filter(id=user_id).values())

        auth_user = request.user

        if auth_user.is_authenticated and auth_user.is_admin:
            if len(users) > 0:
                user = User.objects.get(id=user_id)
                user.username = jd['username']
                user.password = make_password(jd['password'])
                user.save()
                data = {'message': "Success"}
                return Response(data=data, status=ST_200)
            else:
                data = {'message': "User not found..."}
                return Response(data=data, status=ST_404)

        else:
            data = {'message': "You do not have permissions."}
            return Response(data=data, status=ST_403)