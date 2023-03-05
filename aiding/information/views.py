from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from .models import Resource
import  json

class ResourceView(View):
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, id=0):
        if(id > 0):
            resources = list(Resource.objects.filter(id=id).values())
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
            return JsonResponse(resources, safe=False)

    def post(self, request):

        jd = json.loads(request.body)

        street = jd['street']
        number = str(jd['number'])
        city = jd['city']
        
        address = street +", "+ number+", "+city
        latitude = jd['latitude']
        longitude = jd['longitude']

        if latitude is None or longitude is None:

            url = f'https://nominatim.openstreetmap.org/search?q={address}&format=json'

            response = request.get(url).json()
            latitude = response[0]['lat']
            longitude = response[0]['lon']


        Resource.objects.create(title=jd['title'],description=jd['description'],street=street,number=number,city=city,additional_comments=jd['additional_comments'],latitude=latitude,longitude=longitude)
        data = {'message': "Success"}
        JsonResponse(data)

    def put(self, request, id):
        jd = json.loads(request.body)
        resources = list(Resource.objects.filter(id=id).values())
        if len(resources) > 0:
            resource = Resource.objects.get(id=id)
            resource.title = jd['title']
            resource.description = jd['description']
            resource.street = jd['street']
            resource.number = jd['number']
            resource.city = jd['city']
            resource.additional_comments = jd['additional_comments']

            street = jd['street']
            number = str(jd['number'])
            city = jd['city']
        
            address = street +", "+ number+", "+city
            latitude = jd['latitude']
            longitude = jd['longitude']


            if latitude is None or longitude is None:

                url = f'https://nominatim.openstreetmap.org/search?q={address}&format=json'

                response = request.get(url).json()
                latitude = response[0]['lat']
                longitude = response[0]['lon']

            resource.latitude = latitude
            resource.longitude = longitude

            resource.save()

    def delete(self, request, id):
        resources = list(Resource.objects.filter(id=id).values())
        if len(resources) > 0:
            Resource.objects.filter(id=id).delete()
            data = {'message': "Success"}
        else:
            data = {'message': "Resource not found..."}
        return JsonResponse(data)

       
