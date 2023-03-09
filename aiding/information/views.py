import json
import urllib.parse

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from geopy.geocoders import Nominatim
from .models import Resource

class ResourceView(View):
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, resource_id=0):
        if(id > 0):
            resources = list(Resource.objects.filter(resource_id=id).values())
            if len(resources) > 0:
                resource = resources[0]
                data = {'resource': resource}
            else:
                data = {'message': "Resource not found..."}
            
            return JsonResponse(resources, safe = False)
        else:
            resources = list(Resource.objects.values())
            if len(resources) > 0:
                data = {'resources': resources}
            else:
                data = {'message': "Resources not found..."}
            return JsonResponse(resources, safe = False)
            

    def post(self, request):

        jd = json.loads(request.body)
        street = jd['street']
        number = jd['number']
        city = jd['city']
        
        coord = Resource.get_coordinates(street, number, city)
        if isinstance(coord, JsonResponse):
            return coord
        Resource.objects.create(title=jd['title'],description=jd['description'],street=street,number=number,city=city,additional_comments=jd['additional_comments'],latitude=coord[0],longitude=coord[1])
        data = {'message': "Success"}
        return JsonResponse(data)

    def put(self, request, resource_id):
        jd = json.loads(request.body)
        resources = list(Resource.objects.filter(resource_id=id).values())
        if len(resources) > 0:
            resource = Resource.objects.get(id=id)
            resource.title = jd['title']
            resource.description = jd['description']
            resource.additional_comments = jd['additional_comments']

            street = jd['street']
            number = jd['number']
            city = jd['city']
        
            coord = Resource.get_coordinates(street, number, city)
            if isinstance(coord, JsonResponse):
                return coord

            resource.number = number
            resource.street = street
            resource.city = city

            resource.latitude = coord[0]
            resource.longitude = coord[1]

            resource.save()
            data = {'message': "Success"}

            return JsonResponse(data)

    def delete(self, request, resource_id):
        resources = list(Resource.objects.filter(resource_id=id).values())
        if len(resources) > 0:
            Resource.objects.filter(id=id).delete()
            data = {'message': "Success"}
        else:
            data = {'message': "Resource not found..."}
        return JsonResponse(data)
    

