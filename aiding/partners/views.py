from datetime import datetime
import json
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError

from django.http.response import JsonResponse
from .models import Partners, Donation, Communication

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
    
    def get(self, request, communication_id=0, partner_id = 0):
        communications = Communication.objects
        if partner_id > 0:
            communications = communications.filter(partner=partner_id)
            if communication_id>0:
                communications = communications.filter(id=communication_id)
            else:
                return JsonResponse(list(communications.values()), safe = False)
        return JsonResponse(list(communications.values()), safe = False)

    def post(self, request, partner_id):
        jd = json.loads(request.body)
        part = Partners.objects.filter(id = partner_id)
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
        
    def put(self, request, communication_id, partner_id):
        jd = json.loads(request.body)
        communications = Communication.objects.filter(id=communication_id)
        if len(list(communications.values())) > 0:
            part = Partners.objects.filter(id = partner_id)
            if len(part) > 0:
                part = part[0]
                communication = Communication.objects.get(id=communication_id)
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
        
    
    def delete(self, request, communication_id, partner_id):
        communications = Communication.objects.filter(partner=partner_id)
        if len(list(communications.values())) > 0:
            communications = communications.filter(id=communication_id)
            if len(list(communications.values())) > 0:
                communications.delete()
                data = {'message': 'Success'}
            else:
                data = {'message': 'Communication not found...'}
        else:
            data = {'message': 'Partner not found...'}
        return JsonResponse(data)