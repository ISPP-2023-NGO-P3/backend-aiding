import json
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

from rest_framework import views
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK as ST_200,
    HTTP_401_UNAUTHORIZED as ST_401
)

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