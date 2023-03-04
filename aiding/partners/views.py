import json
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.http.response import JsonResponse
from .models import Partner, Donation, DonationType, DonationPeriodicity

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
        part = Partner.objects.filter(id = jd['partner_id'])
        if len(part) > 0:
            date = jd['date']
            donation_type = jd['donation_type']
            amount = jd['amount']
            periodicity = jd['periodicity']
            part = part[0]

            Donation.objects.create(partner=part, date=date, donation_type=donation_type,
                                amount=amount, periodicity=periodicity)
            datos = {'message': "Success"}
        else:

            datos = {'message': "Advertisements not found"}
        return JsonResponse(datos)
    
    def put(self, request, id):
        jd = request.POST
        donations = list(Donation.objects.filter(id=id).values())
        if len(donations) > 0:
            partner =Partner.objects.filter(id = jd['partner_id'])
            partner = partner[0]
            donation = Donation.objects.get(id=id)
            donation.partner = partner
            donation.date = jd['date']
            donation.donation_type = jd['donation_type']
            donation.amount = jd['amount']
            donation.periodicity = jd['periodicity']
            donation.save()
            datos = {'message': "Success"}
        else:
            datos = {'message': "Donation not found..."}
        return JsonResponse(datos)

class PartnerView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id = 0):
        if (id > 0):
            partners = list(Partner.objects.filter(id=id).values())
            if len(partners) > 0:
                partners = partners[0]
                datos = {'partners': partners}
            else:
                datos = {'message': "partner not found..."}
            return JsonResponse(partners, safe = False)
        else:
            partners = list(Partner.objects.values())
            if len(partners) > 0:
                datos = {'partners': partners}
            else:
                datos = {'message': "partners not found..."}
            return JsonResponse(partners, safe = False)

    def post(self, request):
        jd = json.loads(request.body)
        Partner.objects.create(name=jd['name'])
        data = {'message': 'Success'}
        return JsonResponse(data)

    def put(self, request, id):
        name = request.POST.get('name', '')
        partners = list(Partner.objects.filter(id=id).values())
        if len(partners) > 0:
            partner = Partner.objects.get(id=id)
            partner.name = name
            partner.save()
            data = {'message': 'Success'}
        else:
            data = {'message': 'Partner not found...'}
        return JsonResponse(data)

    def delete(self, request, id):
        partners = list(Partner.objects.filter(id=id).values())
        if len(partners) > 0:
            Partner.objects.filter(id=id).delete()
            data = {'message': 'Success'}
        else:
            data = {'message': 'Partner not found...'}
        return JsonResponse(data)