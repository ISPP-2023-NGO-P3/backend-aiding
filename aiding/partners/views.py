import json

from django.shortcuts import render

from django.views import View
from django.views.decorators.csrf import csrf_exempt

from django.utils.decorators import method_decorator

from django.http.response import JsonResponse


from models import Communication, CommunicationType, Partner

# Create your views here.

class CommunicationView(View):
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, id=0):
        if id>0:
            communications =list(Communication.objects(id=id).values())
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
        part = Partner.objects.filter(id = jd['communication_id'])
        if len(part) > 0:
            date = jd['date']
            communication_type=jd['communication_type']

            Communication.objects.create(partner=part, date=date,
                                         communication_type=communication_type)
            datos={'message':"Success"}
        else:
            datos={'message':"Communications not found"}
        return JsonResponse(datos)
    
    def put(self, request, id):
        jd = request.POST
        communications = list(Communication.objects.filter(id= id).values)
        if len(communications)>0:
            partner = Partner.objects.filter(id = jd['partner_id'])
            partner = partner[0]
            communication = Communication.objects.get(id=id)
            communication.partner = partner
            communication.date = jd['date']
            communication.communication_type= jd['communication_type']
            communication.save()
            datos = {'message': "Success"}
        else:
            datos={'message': "Communication not found"}
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