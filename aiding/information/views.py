from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from .models import Resource
import  json
# Create your views here.

class ResourceView(View):
    
    def get(self, request, id=0):
        if(id > 0):
            resources = list(Resource.objects.filter(id=id).values())
            if len(resources) > 0:
                resource = resources[0]
                datos = {'resource': resource}
            else:
                datos = {'message': "resource not found."}
            return JsonResponse(datos, safe = False)

    def post(self, request):

        req = json.loads(request.body)
        street = req['street']
        number = req['number']
        city = req['city']
        address = street +", "+ number+", "+city
        
        url = f'https://nominatim.openstreetmap.org/search?q={address}&format=json'
        response = request.get(url).json()
        latitude = response[0]['lat']
        longitude = response[0]['lon']


        Resource.objects.create(title=req['title'],description=req['description'],street=street,number=number,city=city,additional_comments=req['additional_comments'],latitude=latitude,longitude=longitude)
