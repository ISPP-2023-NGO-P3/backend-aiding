from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json

class LoginView(View):
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
        else:
            data = {'message' : 'Login unsuccessful'}
        
        return JsonResponse(data)

class LogoutView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request):
        jd = json.loads(request.body)
        if request.user.is_authenticated:
            logout(request)
            data = {'message' : 'Logout successful!'}
        else:
            data = {'message' : 'Logout unsuccessful'}
        return JsonResponse(data)
        
        