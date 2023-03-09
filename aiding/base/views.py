from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import json

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

    def post(self, request):
        jd = json.loads(request.body)
        user = authenticate(username = jd['username'], password = jd['password'])
        print(user)
        if user is not None:
            login(request, user)
            data = {'message' : 'Login successful!'}
            return Response(data, status=ST_200)
        else:
            data = {'message' : 'Login unsuccessful'}
            return Response(data, status=ST_401)

class LogoutView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
            data = {'message' : 'Logout successful!'}
        else:
            data = {'message' : 'Logout unsuccessful'}
        return Response(data, status=ST_200)