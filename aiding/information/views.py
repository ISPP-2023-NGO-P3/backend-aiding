from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from .models import Resource
from geopy.geocoders import Nominatim


import  json, urllib, urllib.parse

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
            
            r = JsonResponse(resources, safe = False)
            return r
        else:
            resources = list(Resource.objects.values())
            if len(resources) > 0:
                data = {'resources': resources}
            else:
                data = {'message': "Resources not found..."}
            r = JsonResponse(resources, safe = False)
            return r

    def get_coordinates(self, street, number, city):
        address = street
                   
        if number:
            if number.isdigit():
                if int(number)>0:
                    address += ", " + number
                else:
                    return JsonResponse({'error': "Number must be positive or null"})
            else:
                return JsonResponse({'error': "Number must be positive or null"})

        address += ", "+ city
        geolocator = Nominatim(user_agent="aiding")
        location = geolocator.geocode(address)

        if location:
            latitude = location.latitude
            longitude = location.longitude
        else:
            return JsonResponse({'error': "Address not found"})
        print(latitude)
        print(longitude)

        return latitude, longitude

    @staff_member_required
    def post(self, request):

        jd = json.loads(request.body)
        street = jd['street']
        number = jd['number']
        city = jd['city']
        
        coord = self.get_coordinates(street, number, city)
        if isinstance(coord, JsonResponse):
            return coord
        Resource.objects.create(title=jd['title'],description=jd['description'],street=street,number=number,city=city,additional_comments=jd['additional_comments'],latitude=coord[0],longitude=coord[1])
        data = {'message': "Success"}
        return JsonResponse(data)

    @staff_member_required
    def put(self, request, id):
        jd = json.loads(request.body)
        resources = list(Resource.objects.filter(id=id).values())
        if len(resources) > 0:
            resource = Resource.objects.get(id=id)
            resource.title = jd['title']
            resource.description = jd['description']
            resource.additional_comments = jd['additional_comments']

            street = jd['street']
            number = jd['number']
            city = jd['city']
        
            coord = self.get_coordinates(street, number, city)
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

    @staff_member_required
    def delete(self, request, id):
        resources = list(Resource.objects.filter(id=id).values())
        if len(resources) > 0:
            Resource.objects.filter(id=id).delete()
            data = {'message': "Success"}
        else:
            data = {'message': "Resource not found..."}
        return JsonResponse(data)

       
