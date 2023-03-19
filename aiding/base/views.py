from django.db import IntegrityError
from rest_framework import views
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator 
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK as ST_200,
    HTTP_201_CREATED as ST_201,
    HTTP_404_NOT_FOUND as ST_404,
    HTTP_409_CONFLICT as ST_409,
    HTTP_204_NO_CONTENT as ST_204
)
import json
from .models import Contact


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
            
    def post(self,request):
        jd = json.loads(request.body)
        Contact.objects.create(
            name=jd['name'],
            email=jd['email'],
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