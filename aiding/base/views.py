from django.core.mail import EmailMultiAlternatives
import json
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from rest_framework import views
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK as ST_200,
    HTTP_201_CREATED as ST_201,
    HTTP_403_FORBIDDEN as ST_403,
    HTTP_404_NOT_FOUND as ST_404,
    HTTP_409_CONFLICT as ST_409,
    HTTP_204_NO_CONTENT as ST_204,
    HTTP_400_BAD_REQUEST as ST_400,
    HTTP_205_RESET_CONTENT as ST_205,
    HTTP_401_UNAUTHORIZED as ST_401,
)
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import IntegrityError

from aiding.settings import EMAIL_HOST_USER
from django.utils.encoding import smart_str
from unidecode import unidecode
from .models import Contact, User
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login
from django.core.files.base import ContentFile
from django.utils.text import slugify

class RoleView(views.APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        role = None
        if user.is_admin:
            role = 'admin'
        elif user.roles != None:
            role = str(request.user.roles)
        else:
            role = 'user'

        data = {'role': role}
        return Response(data=data, status=ST_200)

class RolesView(views.APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, section_id=0):
        groups = list(Group.objects.all().values())
        lenght = len(groups)
        if lenght > 0:
            return Response(data=groups, status=ST_200)
        else:
            datos = {"message": "groups not found..."}
            return Response(data=datos, status=ST_404)
        
class LoginView(views.APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, args, **kwargs):
        return super().dispatch(request,args, **kwargs)

    @method_decorator(csrf_exempt)
    def post(self, request):
        if request.user.is_authenticated:
            data = {'message' : 'You are already logged in'}
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
    @method_decorator(login_required)
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=ST_205)
        except Exception as e:
            print(e)
            return Response(status=ST_400)

class RegisterView(views.APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        jd = json.loads(request.body)
        username = jd['username']
        password = jd['password']
        password2 = jd['password2']

        if password != password2:
            data = {'message': 'Passwords do not match'}
            return Response(data=data, status=ST_409)
        
        try:
            user = User.objects.create(username=username, password=make_password(password), is_admin=False)
            user.save()

            userAuth = authenticate(username=username, password=password)
            login(request, userAuth)
            return Response(status=ST_201)
        except IntegrityError:
            data = {'message': 'Username already exists'}
            return Response(data=data, status=ST_409)

class UserView(views.APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @method_decorator(login_required)
    def get(self, request, user_id=0):
        if (user_id > 0):
            users = list(User.objects.filter(id=user_id).values())
            if len(users) > 0:
                user = users[0]
                print(user['password'])
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

    @method_decorator(login_required)
    def post(self, request):
        jd = json.dumps(request.data)
        jd = json.loads(jd)
        auth_user = request.user
        if auth_user.is_authenticated and auth_user.is_admin:
            roles_id = request.POST.get('roles_id')
            error = {"error": "Role ID not provided"}
            print(roles_id)
                # return Response(data=error, status=ST_400)
            try:
                if(roles_id== '' or roles_id== None):
                    try:
                        User.objects.create(username=request.POST.get('username'), password=make_password(
                        request.POST.get('password')), is_admin=jd.get('is_admin', False))
                        data = {'message': "Success"}
                        return Response(data=data, status=ST_201)
                    except IntegrityError:
                        data = {'message': 'Username already exists'}
                        return Response(data=data, status=ST_409)
                else:
                    role = Group.objects.get(name=jd['roles_id'])
                    try: 
                        User.objects.create(username=request.POST.get('username'), password=make_password(
                        request.POST.get('password')), is_admin=jd.get('is_admin', False), roles=role)
                        data = {'message': "Success"}
                        return Response(data=data, status=ST_201)
                    except IntegrityError:
                        data = {'message': 'Username already exists'}
                        return Response(data=data, status=ST_409)
            except Group.DoesNotExist:
                error = {
                "error": "Type not found"
            }
            return Response(data=error, status=ST_404)
        else:
            data = {'message': "You do not have permissions."}
            return Response(data=data, status=ST_403)

    @method_decorator(login_required)
    def put(self, request, user_id):
        jd = json.dumps(request.data)
        jd = json.loads(jd)
        users = list(User.objects.filter(id=user_id).values())
        auth_user = request.user
        if auth_user.is_authenticated and auth_user.is_admin:
            roles_id = jd['roles_id']
            error = {"error": "Role ID not provided"}
            if len(users) > 0:
                try:
                    user = User.objects.get(id=user_id)
                    old_password = request.data.get('password')
                    if user.check_password(old_password):
                        if(roles_id== '' or roles_id== None):
                            user = User.objects.get(id=user_id)
                            user.username = jd['username']
                            new_password = request.data.get('new_password')
                            old_password = request.data.get('password')
                            if user.check_password(old_password) and new_password and new_password != old_password:
                                user.password = make_password(new_password)
                            user.is_admin = jd['is_admin']
                            user.roles = None
                            user.save()
                            data = {'message': "Success"}
                            return Response(data=data, status=ST_200)
                        else:
                            role = Group.objects.get(id=jd['roles_id'])
                            user = User.objects.get(id=user_id)
                            user.username = jd['username']
                            new_password = request.data.get('new_password')
                            old_password = request.data.get('password')
                            if user.check_password(old_password) and new_password and new_password != old_password:
                                user.password = make_password(new_password)
                            user.is_admin = jd['is_admin']
                            user.roles = role
                            user.save()
                            data = {'message': "Success"}
                            return Response(data=data, status=ST_201)
                except Group.DoesNotExist:
                        error = {
                        "error": "Type not found"
                    }   
                return Response(data=error, status=ST_404)
            else:
                data = {'message': "User not found..."}
                return Response(data=data, status=ST_404)

        else:
            data = {'message': "You do not have permissions."}
            return Response(data=data, status=ST_403)

class ContactView(views.APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, contact_id=0):
        if (contact_id > 0):
            contacts = list(Contact.objects.filter(id=contact_id).values())
            if len(contacts) > 0:
                contacts = contacts[0]
                return Response(data=contacts, status=ST_200)
            else:
                datos = {'message': "partner not found..."}
            return Response(data=datos, status=ST_404)
        else:
            contacts = list(Contact.objects.all().values())
            if len(contacts) > 0:
                datos = {'contacts': contacts}
                return Response(data=contacts, status=ST_200)
            else:
                datos = {'message': "contacts not found..."}
            return Response(data=datos, status=ST_404)

    def post(self, request):
        jd = json.loads(request.body)
        Contact.objects.create(
            name=jd['name'],
            email=jd['email'],
            phone=jd['phone'],
            subject=jd['subject'],
            message=jd['message'],
        )
        datos = {'message': "contact created..."}
        return Response(data=datos, status=ST_201)

    def delete(self, request, contact_id):
        contacts = list(Contact.objects.filter(id=contact_id).values())
        if len(contacts) > 0:
            Contact.objects.filter(id=contact_id).delete()
            datos = {'message': "Success..."}
            return Response(data=datos, status=ST_204)
        else:
            datos = {'message': "Delete not found..."}
            return Response(data=datos, status=ST_404)

    def put(self, request, contact_id):
        jd = json.loads(request.body)
        contacts = list(Contact.objects.filter(id=contact_id).values())
        if len(contacts) > 0:
            contact = Contact.objects.get(id=contact_id)
            try:
                contact.isAnswered = jd['isAnswered']
                contact.save()
                datos = {'message': "Success..."}
                return Response(data=datos, status=ST_200)
            except IntegrityError:
                datos = {'message': "Error..."}
                return Response(data=datos, status=ST_409)
        else:
            datos = {'message': "Update not found..."}
            return Response(data=datos, status=ST_404)
        
class NotificationView(views.APIView):

    # permission_classes = [IsAdminUser]

    def send_notification(recipients, subject, message, attached_file=None):

        recipients = [smart_str(recipients) for recipients in recipients]
        subject = smart_str(subject)
        message = smart_str(message)

        recipients = [unidecode(recipients) for recipients in recipients]
        subject = unidecode(subject)
        message = unidecode(message)

        email = EmailMultiAlternatives(
            subject=subject,
            body=message,
            from_email=unidecode(EMAIL_HOST_USER),
            to=recipients,
        )

        if attached_file:
            file_name = slugify(attached_file.name)
            file_content = ContentFile(attached_file.read().decode('latin-1'))
            email.attach(file_name, file_content.read(), attached_file.content_type)
        try:
            email.send(fail_silently=False)
        except Exception as e:
            raise e;

    def post(self,request):
        recipients = request.POST.get('recipients').split(' ')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        _file = request.FILES.get('file')
        try:
            NotificationView.send_notification(recipients, subject, message, _file)
            datos = {'message': "notification sended..."}
            return Response(data=datos, status=ST_201)
        
        except Exception:
            datos = {'message': "Error..."}
            return Response(data=datos, status=ST_401)
        