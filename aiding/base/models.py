from django.db import models
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json

# Create your views here.

class UserView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, id = 0):
        if (id > 0):
            users = list(User.objects.filter(id=id).values())
            if len(users) > 0:
                user = users[0]
                data = {'user': user}
            else:
                data = {'message': "user not found..."}
            return JsonResponse(user, safe = False)
        else:
            users = list(User.objects.values())
            if len(users) > 0:
                data = {'users': users}
            else:
                data = {'message': "users not found..."}
            return JsonResponse(users, safe = False)
        
    def post(self, request):
        auth_user = request.user
        if auth_user.is_authenticated() and auth_user.role == 'ADMIN':
            jd = json.loads(request.body)
            User.objects.create(username=jd['username'],password=jd['password'])
            data = {'message': "Success"}
            return JsonResponse(data)
        else:
            data = {'message': "You do not have permissions."}
            return JsonResponse(data)

    def put(self, request, id):
        jd = json.loads(request.body)
        users = list(User.objects.filter(id=id).values())
        
        auth_user = request.user
        
        if auth_user.is_authenticated() and auth_user.role == 'ADMIN':
            if len(users) > 0:
                user = User.objects.get(id=id)
                user.username = jd['username']
                user.password = jd['password']
                user.save()
                data = {'message': "Success"}
            else:
                data = {'message': "User not found..."}
            return JsonResponse(data)
        
        else:
            data = {'message': "You do not have permissions."}
            return JsonResponse(data)