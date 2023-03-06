import json
from django.forms import ValidationError
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.db import IntegrityError


class PartnerManagement(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, id = 0):
        if (id > 0):
            partners = list(Partners.objects.filter(id=id).values())
            if len(partners) > 0:
                partners = partners[0]
                datos = {'partners': partners}
            else:
                datos = {'message': "partner not found..."}
            return JsonResponse(partners, safe = False)
        else:
            partners = list(Partners.objects.values())
            if len(partners) > 0:
                datos = {'partners': partners}
            else:
                datos = {'message': "partners not found..."}
            return JsonResponse(partners, safe = False)
        
    def post(self, request):
        jd = json.loads(request.body)

        try:
            validate_dni(jd['dni'])
        except ValidationError as e:
            error = {'error': e.message}
            return JsonResponse(error)
    
        #try:
        #    validate_iban(jd['iban'])
        #except ValidationError as e:
        #    error = {'error': e.message}
        #    return JsonResponse(error)

        try:
            Partners.objects.create(name=jd['name'], last_name=jd['last_name'], 
            dni=jd['dni'], phone1=jd['phone1'], phone2=jd['phone2'], birthdate=jd['birthdate'], sex=jd['sex'],
            email=jd['email'], address=jd['address'], postal_code=jd['postal_code'], township=jd['township'],
            province=jd['province'], language=jd['language'], iban=jd['iban'],  account_holder=jd['account_holder'],
            state=jd['state'])
            datos = {'message': "Success"}
            return JsonResponse(datos)
        except IntegrityError:
            error = {'error': "There is already a partner with a field equal to the one you are trying to add, please check the data."}
            return JsonResponse(error)

    def put(self, request, id):
        jd = json.loads(request.body)
        partners = list(Partners.objects.filter(id=id).values())
        if len(partners) > 0:
            partner = Partners.objects.get(id=id)
            try:
                validate_dni(jd['dni'])
            except ValidationError as e:
                error = {'error': e.message}
                return JsonResponse(error)
            
            #try:
            #    validate_iban(jd['iban'])
            #except ValidationError as e:
            #    error = {'error': e.message}
            #    return JsonResponse(error)
        
            partner.name = jd['name']
            partner.last_name=jd['last_name']
            partner.dni=jd['dni']
            partner.phone1=jd['phone1']
            partner.phone2=jd['phone2']
            partner.birthdate=jd['birthdate']
            partner.sex=jd['sex']
            partner.address=jd['address']
            partner.postal_code=jd['postal_code']
            partner.township=jd['township']
            partner.email=jd['email']
            partner.province=jd['province']
            partner.language=jd['language']
            partner.iban=jd['iban']
            partner.account_holder=jd['account_holder']
            partner.state=jd['state']
            partner.save()
            datos = {'message': "Success"}
        else:
            datos = {'message': "Partner not found..."}
        return JsonResponse(datos)