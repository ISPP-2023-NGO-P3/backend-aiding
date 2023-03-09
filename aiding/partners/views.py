
from datetime import datetime
import json
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.db import IntegrityError

from django.http.response import JsonResponse
from .models import Partners, Donation

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
            Partners.objects.create(name=jd['name'], last_name=jd['last_name'], 
            dni=jd['dni'], phone=jd['phone'], email=jd['email'], province=jd['province'],
            iban=jd['iban'], state=jd['state'])
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
            partner.name = jd['name']
            partner.last_name=jd['last_name']
            partner.dni=jd['dni']
            partner.phone=jd['phone']
            partner.email=jd['email']
            partner.province=jd['province']
            partner.iban=jd['iban']
            partner.state=jd['state']
            partner.save()
            datos = {'message': "Success"}
        else:
            datos = {'message': "Partner not found..."}
        return JsonResponse(datos)
    


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


class CommunicationView(View):
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, id=0):
        if id>0:
            communications =list(Communication.objects.filter(id=id).values())
            if len(communications) > 0:
                communication = communications[0]
                datos = {'communication': communication}
            else:
                datos = {'message': "Communication not found"}
            return JsonResponse(communication, safe = False)
        else:
            communications = list(Communication.objects.values())
            if len(communications)>0:
                datos = {'communications': communications}
            else:
                datos = {'message': "Communications not found"}
            return JsonResponse(communications, safe = False)
        
    def post(self, request):
        jd = json.loads(request.body)
        part = Partners.objects.filter(id = jd['partner'])
        if len(part) >0:
            part = part[0]
            date = jd['date']
            communication_type=jd['communication_type']
            description = jd['description']

            Communication.objects.create(partner=part, date=date,
                                            communication_type=communication_type, description =description)

            data = {'message': 'Success'}
        else:
            data = {'message': 'Partner not found'}
        return JsonResponse(data)
        
    def put(self, request, id):
        jd = json.loads(request.body)
        communications = list(Communication.objects.filter(id=id).values())
        if len(communications) > 0:
            part = Partners.objects.filter(id = jd['partner_id'])
            if len(part) > 0:
                part = part[0]
                communication = Communication.objects.get(id=id)
                communication.partner = part
                communication.date = jd['date']
                communication.communication_type = jd['communication_type']
                communication.description = jd['description']
                communication.save()
                datos = {'message': "Success"}
            else:
                datos = {'message': "Partner not found..."}
        else:
            datos = {'message': "Communication not found..."}
        return JsonResponse(datos)
        
    
    def delete(self, request, id):
        communications = list(Communication.objects.filter(id=id).values())
        if len(communications) > 0:
            Communication.objects.filter(id=id).delete()
            data = {'message': 'Success'}
        else:
            data = {'message': 'Communication not found...'}
        return JsonResponse(data)