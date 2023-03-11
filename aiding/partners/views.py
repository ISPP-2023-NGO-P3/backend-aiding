from datetime import datetime
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from django.forms import ValidationError
from django.db import IntegrityError
from django.http.response import JsonResponse
from .models import Partners, Donation
from validators import validate_date, validate_dni, validate_iban

from rest_framework import views
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK as ST_200,
    HTTP_201_CREATED as ST_201,
    HTTP_404_NOT_FOUND as ST_404,
    HTTP_409_CONFLICT as ST_409,
)

class PartnerManagement(views.APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, id = 0):
        if (id > 0):
            partners = list(Partners.objects.filter(id=id).values())
            if len(partners) > 0:
                partners = partners[0]
                return Response(data=partners, status=ST_200)
            else:
                datos = {'message': "partner not found..."}
            return Response(data=datos, status=ST_404)
        else:

            partners = list(Partners.objects.values())
            if len(partners) > 0:
                datos = {'partners': partners}
                return Response(data=partners, status=ST_200)
            else:
                datos = {'message': "partners not found..."}
            return Response(data=datos, status=ST_404)
  
    def post(self, request):
        jd = json.loads(request.body)

        try:
            validate_dni(jd['dni'])
            validate_iban(jd['iban'])
            validate_date(jd['birthdate'])
        except ValidationError as e:
            error = {'error': e.message}
            return Response(data=error, status=ST_409)

        try:
            Partners.objects.create(name=jd['name'], last_name=jd['last_name'], 
            dni=jd['dni'], phone1=jd['phone1'], phone2=jd['phone2'], birthdate=jd['birthdate'], sex=jd['sex'],
            email=jd['email'], address=jd['address'], postal_code=jd['postal_code'], township=jd['township'],
            province=jd['province'], language=jd['language'], iban=jd['iban'],  account_holder=jd['account_holder'],
            state=jd['state'], observations=jd['observations'])
            datos = {'message': "Success"}
            return Response(data=datos, status=ST_201)
        except IntegrityError:
            error = {'error': "There is already a partner with a field equal to the one you are trying to add, please check the data."}
            return Response(data=error, status=ST_409)

    def put(self, request, id):
        jd = json.loads(request.body)
        partners = list(Partners.objects.filter(id=id).values())
        if len(partners) > 0:
            partner = Partners.objects.get(id=id)
            try:
                validate_dni(jd['dni'])
                validate_iban(jd['iban'])
                validate_date(jd['birthdate'])
            except ValidationError as e:
                error = {'error': e.message}
                return Response(data=error, status=ST_409)
            try:   
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
                partner.observations=jd['observations']
                partner.save()
                datos = {'message': "Success"}
                return Response(data=datos, status=ST_200)
            except:
                error = {'error': "There is already a partner with a field equal to the one you are trying to add, please check the data."}
                return Response(data=error, status=ST_409)

        else:
            datos = {'message': "Partner not found..."}
        return Response(data=error, status=ST_409)
    

class DonationView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if id > 0:
            donations = list(Donation.objects.filter(id=id).values())
            if len(donations) > 0:
                donation = donations[0]
                datos = {'donation': donation}
            else:
                datos = {'message': "Donation not found..."}
            return JsonResponse(donation, safe=False)
        else:
            donations = list(Donation.objects.values())
            if len(donations) > 0:
                datos = {'donations': donations}
            else:
                datos = {'message': "Donations not found..."}
            return JsonResponse(donations, safe=False)
        
    def post(self, request):
        jd = json.loads(request.body)
        partner_id = jd['partner_id']
        donation_type = jd['donation_type']
        amount = jd['amount']
        periodicity = jd['periodicity']

        try:
            partner = Partners.objects.get(id=partner_id, state='ACTIVE')
        except Partners.DoesNotExist:
            datos = {'message': "Partner not found or not active"}
            return JsonResponse(datos, status=400)

        date_str = jd['date']
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        Donation.objects.create(partner=partner, date=date, donation_type=donation_type,
                                amount=amount, periodicity=periodicity)

        datos = {'message': "Success"}
        return JsonResponse(datos)

    
    def put(self, request, id):
        jd = json.loads(request.body)
        donations = list(Donation.objects.filter(id=id).values())
        if len(donations) > 0:
            partner =Partners.objects.filter(id = jd['partner_id'])
            partner = partner[0]
            donation = Donation.objects.get(id=id)
            donation.partner = partner
            donation.periodicity = jd['periodicity']
            donation.save()
            datos = {'message': "Success"}
        else:
            datos = {'message': "Donation not found..."}
        return JsonResponse(datos)
    
    def delete(self, request, id):
        try:
            donation = Donation.objects.get(id=id)
            donation.delete()
            datos = {'message': "Success"}
        except Donation.DoesNotExist:
            datos = {'message': "Donation not found..."}
        return JsonResponse(datos)

